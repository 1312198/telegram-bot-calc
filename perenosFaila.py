import os
import shutil

# Исходная папка
source_folder = 'E:\\Флорентина фото'
# Целевая папка
target_folder = 'E:\\Флорентина фото\\Схемы'

# Проверяем существование целевой папки, создаем если нет
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Перебираем все файлы в исходной папке
for filename in os.listdir(source_folder):
    # Проверяем наличие подстроки "-схема" в имени файла
    if '-интерьер' in filename.lower():
        # Формируем полный путь к файлу
        source_file = os.path.join(source_folder, filename)
        target_file = os.path.join(target_folder, filename)
        
        # Перемещаем файл
        try:
            shutil.move(source_file, target_file)
            print(f'Файл {filename} перемещен в папку Схемы')
        except Exception as e:
            print(f'Ошибка при перемещении файла {filename}: {e}')
