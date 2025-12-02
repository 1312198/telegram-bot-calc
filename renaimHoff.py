import os
import pandas as pd

# Путь к Excel файлу
excel_file_path = r'C:\Users\Михаил\Downloads\при\Матрица.xlsx'
# Путь к папке с файлами для обработки
folder_path = r'C:\Users\Михаил\Downloads\obrabotka'

# Читаем Excel файл
df = pd.read_excel(excel_file_path)

# Проходим по всем строкам DataFrame
for index, row in df.iterrows():
    # Получаем значения из второго и первого столбцов
    if pd.isna(row[1]):  # Проверяем на пустую строку
        break
    old_value = str(row[1])  # Преобразуем в строку
    new_value = str(row[0])  # Преобразуем в строку

    # Проходим по всем файлам в указанной папке
    for filename in os.listdir(folder_path):
        if old_value in filename:
            # Заменяем старое значение на новое
            new_filename = filename.replace(old_value, new_value)
            # Полные пути к старому и новому файлам
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            # Переименовываем файл
            os.rename(old_file_path, new_file_path)
            print(f'Переименован: {old_file_path} -> {new_file_path}')
