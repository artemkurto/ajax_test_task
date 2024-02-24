def parse_log_file(log_file_path):
    sensor_counts = {}
    successful_sensor_ids = set()
    failed_sensor_ids = set()

    with open(log_file_path, 'r') as file:
        for line in file:
            if 'BIG' in line:
                parts = line.strip().split(';')
                sensor_id = parts[2]
                state = parts[-2]
                if state == '02':
                    successful_sensor_ids.add(sensor_id)
                    sensor_counts[sensor_id] = sensor_counts.get(sensor_id, 0) + 1
                elif state == 'DD':
                    failed_sensor_ids.add(sensor_id)

    successful_sensor_count = len(successful_sensor_ids)
    failed_sensor_count = len(failed_sensor_ids)

    return sensor_counts, successful_sensor_count, failed_sensor_count


log_file_path = 'app_2.log'
sensor_counts, successful_sensor_count, failed_sensor_count = parse_log_file(log_file_path)

print("Кількість повідомлень з хендлером 'BIG' для кожного датчика, який ОК:")
for sensor_id, count in sensor_counts.items():
    print(f"Датчик {sensor_id}: {count} повідомлень")

print(f"\nЗагальна кількість датчиків, які успішно пройшли тест: {successful_sensor_count}")
print(f"Загальна кількість датчиків, які завалили тест: {failed_sensor_count}")
