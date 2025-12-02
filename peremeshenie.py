import os
import shutil

# Путь к исходной папке
source_folder = r'C:\Users\Михаил\Downloads\WesnaArt новинки март 25'
# Путь к папке, куда будут перемещены изображения
destination_folder = r'C:\Users\Михаил\Downloads\Весна нью'

# Создаем папку назначения, если она не существует
os.makedirs(destination_folder, exist_ok=True)

# Множество для хранения имен перемещенных файлов
moved_files = set()

# Проходим по всем подкаталогам и файлам в исходной папке
for root, dirs, files in os.walk(source_folder):
    for file in files:
        # Проверяем, является ли файл изображением формата jpg или png
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Полный путь к файлу
            file_path = os.path.join(root, file)
            try:
                # Проверяем, был ли файл уже перемещен
                if file in moved_files:
                    print(f'Пропущен (уже перемещен): {file_path}')
                    continue
                
                # Перемещаем файл в папку назначения
                shutil.move(file_path, destination_folder)
                # Добавляем имя файла в множество перемещенных файлов
                moved_files.add(file)
                print(f'Перемещен: {file_path} -> {destination_folder}')
            except Exception as e:
                print(f'Ошибка при перемещении файла {file_path}: {e}')

print('Перемещение изображений завершено.')

