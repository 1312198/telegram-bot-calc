import os
import pandas as pd

# Путь к файлу Excel
excel_file_path = r'C:\Users\Михаил\Desktop\Артикулы\Замены.xlsx'

# Путь к папке с фото
photos_directory = r'C:\Users\Михаил\Desktop\Артикулы\Фото\Смесители для раковины'

# Читаем файл Excel
df = pd.read_excel(excel_file_path)

# Получаем значение из первого столбца первой строки
old_value = str(df.iloc[0, 0])  # Значение из первого столбца, первая строка
new_value = str(df.iloc[0, 1])  # Значение из второго столбца, первая строка

# Список суффиксов для добавления
suffixes = ["-схема.jpg", "-интерьер", "-интерьер1", "-интерьер2", "-интерьер3", 
            "-интерьер4", "-интерьер5", "-интерьер6", "-интерьер7"]

# Проходим по всем суффиксам
for suffix in suffixes:
    search_value = old_value + suffix  # Добавляем суффикс к старому значению
    count = 0  # Счетчик найденных файлов
    renamed_files = []  # Список переименованных файлов

    # Проходим по всем файлам в директории
    for filename in os.listdir(photos_directory):
        # Проверяем на точное вхождение старого значения в названии файла
        if old_value in filename:
            count += 1
            # Формируем новое имя файла, заменяя только точное вхождение
            new_filename = filename.replace(old_value, new_value)
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

# Сообщение о завершении работы
print("Код полностью отработал.")
