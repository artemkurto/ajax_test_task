from unittest.mock import patch
import pytest
from scanner_handler import CheckQr

check_qr = CheckQr()


@pytest.mark.parametrize("qr, expected_color", [
    ('XXX', 'Red',),
    ('XXXXX', 'Green',),
    ('XXXXXXX', 'Fuzzy Wuzzy',),
    ('XX', None),
])
def test_check_scanned_device(qr, expected_color):
    with patch('scanner_handler.CheckQr.check_in_db', return_value=True):
        check_qr.check_scanned_device(qr)
    assert check_qr.color == expected_color


class ModifiedSendError(CheckQr):

    def send_error(self, error: str):
        print(error)
        return super().send_error(error)


modified_send_error = ModifiedSendError()


@pytest.mark.parametrize("qr, value_check_in_db, expected_send_error", [
    ('XXX', True, '',),
    ('XXXX', True, 'Error: Wrong qr length 4\n',),
    ('XXXXX', None, 'Not in DB\n',),
    ('XXXXXX', None, 'Error: Wrong qr length 6\n',)
])
def test_check_send_error(qr, value_check_in_db, expected_send_error, capfd):
    with patch('scanner_handler.CheckQr.check_in_db', return_value=value_check_in_db):
        modified_send_error.check_scanned_device(qr)
        out, _ = capfd.readouterr()
        assert out == expected_send_error


class ModifiedCanAddDevice(CheckQr):

    def can_add_device(self, message: str):
        print(message)
        return super().can_add_device(message)


modified_can_add_device = ModifiedCanAddDevice()


@pytest.mark.parametrize("qr, value_check_in_db, expected_message", [
    ('XXX', None, 'hallelujah XXX\n',),
    ('XXXXX', True, 'hallelujah XXXXX\nhallelujah XXXXX\n'),
    ('XX', None, '',),
    ('XX', True, '',)

])
def test_can_add_device(qr, value_check_in_db, expected_message, capfd):
    with patch('scanner_handler.CheckQr.check_in_db', return_value=value_check_in_db):
        modified_can_add_device.check_scanned_device(qr)
        out, _ = capfd.readouterr()
        assert out == expected_message
