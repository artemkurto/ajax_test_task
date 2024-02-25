def parse_log_file(log_file_path):
    successful_sensors = {}
    failed_sensor_ids = set()

    with open(log_file_path, 'r') as file:
        for line in file:
            if 'BIG' in line:
                parts = line.strip().split(';')
                sensor_id = parts[2]
                state = parts[-2]
                if state == '02':
                    successful_sensors[sensor_id] = successful_sensors.get(sensor_id, 0) + 1
                elif state == 'DD':
                    failed_sensor_ids.add(sensor_id)

    for sensor_id in failed_sensor_ids:
        successful_sensors.pop(sensor_id)
    successful_sensor_count = len(successful_sensors)
    failed_sensor_count = len(failed_sensor_ids)

    print('All big messages: ', successful_sensor_count + failed_sensor_count)
    print('Successful big messages: ', successful_sensor_count)
    print('Failed big messages: ', failed_sensor_count)
    print("Success messages count:")
    for sensor_id, count in successful_sensors.items():
        print(f"{sensor_id}: {count}")


def process_failed_sensors(log_file_path):
    error_messages = {1: 'Battery device error', 2: 'Temperature device error', 3: 'Threshold central error'}

    with open(log_file_path, 'r') as file:
        for line in file:
            if 'BIG' and 'DD' in line:
                parts = line.strip().split(';')
                sensor_id = parts[2]
                sp1 = parts[6][:-1]
                sp2 = parts[13]
                combined_value = sp1 + sp2
                grouped_values = [combined_value[i:i + 2] for i in range(0, len(combined_value), 2)]
                binary_values = [bin(int(value))[2:].zfill(8) for value in grouped_values]
                flags = [binary_value[4] for binary_value in binary_values]
                error_codes = [index + 1 for index, flag in enumerate(flags) if flag == '1']
                if error_codes:
                    error_output = ', '.join(
                        [f"{error_messages[error_code]}" for error_code in error_codes])
                    print(f"{sensor_id}: {error_output}")
                else:
                    print(f"{sensor_id} - Unknown device error")


log_file_path = 'app_2.log'

parse_log_file(log_file_path)

print(' ')
process_failed_sensors(log_file_path)
