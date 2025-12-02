import pandas as pd
import numpy as np
import random

# Укажите путь к Excel файлу
file_path = r'C:\Users\Михаил\Desktop\Артикулы\Артикулы.xlsx'

# Чтение Excel файла
df = pd.read_excel(file_path)

# Функция для замены HB на KV и генерации уникальных случайных чисел
def replace_and_randomize(column):
    # Замена HB на KV
    column = column.str.replace('HB', 'KV', regex=False)
    
    # Нахождение уникальных значений
    unique_values = column.unique()
    
    # Генерация уникальных случайных чисел
    random_numbers = random.sample(range(10000, 99999), len(unique_values))
    
    # Создание словаря соответствий
    mapping = dict(zip(unique_values, random_numbers))
    
    # Замена значений в исходном столбце на новые случайные числа
    return column.map(mapping)

# Применяем функцию к каждому столбцу DataFrame
for col in df.columns:
    df[col] = replace_and_randomize(df[col].astype(str))

# Сохраняем измененный DataFrame обратно в файл
df.to_excel(file_path, index=False)

# Закрытие файла не требуется, так как pandas автоматически управляет этим
print("Выполнено")
