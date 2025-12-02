import os
import pandas as pd

# 1. Собираем все названия файлов без учета расширения
folder_path = r'C:\Users\Михаил\Desktop\Артикулы\Фото\Смесители для раковины'
file_names = [os.path.splitext(file)[0] for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

# 2. Открываем файл Замены.xlsx и берем все значения из первого столбца
excel_path = r'C:\Users\Михаил\Desktop\Артикулы\Замены.xlsx'
df = pd.read_excel(excel_path)
replacement_values = df.iloc[:, 0].astype(str).tolist()  # Преобразуем в список строк

# 3. Проверяем, содержатся ли названия файлов в значениях из Excel
missing_items = [file_name for file_name in file_names if file_name not in replacement_values]

# 4. Публикуем список тех, которые не удалось найти
if missing_items:
    print("Следующие названия файлов не найдены в Excel:")
    for item in missing_items:
        print(f"Значение '{item}' не найдено")
else:
    print("Все названия файлов найдены в Excel.")
