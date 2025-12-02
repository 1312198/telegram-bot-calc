import os
import re
from openpyxl import Workbook

# Папка, из которой будем брать файлы
source_folder = r"C:\Users\Михаил\Desktop\Fiore"
# Папка, куда будем сохранять файл Excel
output_folder = r"C:\Users\Михаил\Desktop\Fiore\Fiore"
# Имя файла Excel
excel_file_name = "Список товаров.xlsx"

# Создаем список для хранения названий файлов
file_names = []

# Проходим по всем файлам и папкам в заданной директории
for root, dirs, files in os.walk(source_folder):
    for file in files:
        # Убираем расширение файла
        file_name, _ = os.path.splitext(file)
        # Добавляем файл в список, если он не содержит указанных подстрок
        if not re.search(r'-схема|-интерьер|-интерьер\d*', file_name):
            file_names.append(file_name)

# Создаем новый Excel файл
wb = Workbook()
ws = wb.active
ws.title = "Список товаров"

# Заполняем первый столбик названиями файлов
for index, name in enumerate(file_names, start=1):
    ws.cell(row=index, column=1, value=name)

# Сохраняем Excel файл
output_path = os.path.join(output_folder, excel_file_name)
wb.save(output_path)

print(f"Список товаров успешно сохранен в {output_path}")