import os
from openpyxl import Workbook

# Укажите путь к папке
adress = input('введи адрес!')
# Укажите путь к папке
folder_path = adress

# Слова, которые нужно исключить из названий файлов
excluded_keywords = ["схема", "интерьер", "управление", "душ", "лейка", "излив"]

# Получаем список файлов в папке
file_names = os.listdir(folder_path)

# Создаем новый Excel файл и активируем лист
wb = Workbook()
ws = wb.active

# Заполняем Excel файл названиями файлов, исключая ненужные
for index, file_name in enumerate(file_names, start=1):
    if not any(keyword in file_name.lower() for keyword in excluded_keywords):
        ws.cell(row=index, column=1, value=file_name)

# Сохраняем файл в той же папке
output_file_path = os.path.join(folder_path, "file_names.xlsx")
wb.save(output_file_path)

print(f"Файл сохранен по пути: {output_file_path}")
