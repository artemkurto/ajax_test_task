from unittest.mock import patch
import pytest
from scanner_handler import CheckQr

check_qr = CheckQr()


@pytest.mark.parametrize("qr, expected_color", [
    ('XXX', 'Red'),
    ('XXXXX', 'Green'),
    ('XXXXXXX', 'Fuzzy Wuzzy'),
    ('XX', None)
])
def test_check_scanned_device_in_db(qr, expected_color):
    with patch('scanner_handler.CheckQr.check_in_db', return_value=True):
        check_qr.check_scanned_device(qr)
    assert check_qr.color == expected_color


@pytest.mark.parametrize("qr, expected_color", [
    ('XXX', 'Red'),
    ('XXXXX', 'Green'),
    ('XXXXXXX', 'Fuzzy Wuzzy'),
    ('XXXXXXXX', None)
])
def test_check_scanned_device_not_in_db(qr, expected_color):
    with patch('scanner_handler.CheckQr.check_in_db', return_value=None):
        check_qr.check_scanned_device(qr)
    assert check_qr.color == expected_color
