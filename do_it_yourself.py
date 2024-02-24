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

    return successful_sensors, successful_sensor_count, failed_sensor_count


log_file_path = 'app_2.log'
sensor_counts, successful_sensor_count, failed_sensor_count = parse_log_file(log_file_path)

print("Кількість повідомлень з хендлером 'BIG' для кожного датчика, який ОК:")
for sensor_id, count in sensor_counts.items():
    print(f"Датчик {sensor_id}: {count} повідомлень")

print(f"Загальна кількість датчиків, які успішно пройшли тест: {successful_sensor_count}")
print(f"Загальна кількість датчиків, які завалили тест: {failed_sensor_count}")
