import os
import pandas as pd

# Путь к файлу Excel
excel_file_path = r'C:\Users\Михаил\Desktop\Артикулы\Замены.xlsx'

# Путь к папке с фото
photos_directory = input('папка с фото____________ВВЕДИ!!!__________')

# Читаем файл Excel
df = pd.read_excel(excel_file_path)

# Проходим по всем строкам DataFrame
for index, row in df.iterrows():
    # Получаем значения из первого и второго столбцов
    old_value = row[0]
    new_value = row[1]
    
    # Если старое значение пустое, выходим из цикла
    if pd.isna(old_value):
        break
    
    # Счетчик для найденных файлов
    count = 0
    renamed_files = []

    # Проходим по всем файлам в директории
    for filename in os.listdir(photos_directory):
        # Проверяем на точное вхождение старого значения в названии файла
        if old_value in filename.split('.'):
            count += 1
            # Формируем новое имя файла
            new_filename = filename.replace(old_value, str(new_value))
            # Путь к старому и новому файлу
            old_file_path = os.path.join(photos_directory, filename)
            new_file_path = os.path.join(photos_directory, new_filename)
            # Переименовываем файл
            os.rename(old_file_path, new_file_path)
            # Добавляем новое имя в список
            renamed_files.append((filename, new_filename))

    # Выводим сообщение о замене
    if count > 0:
        print(f'Найдено {count} файлов. Заменены: {", ".join(f"{old} на {new}" for old, new in renamed_files)}')

