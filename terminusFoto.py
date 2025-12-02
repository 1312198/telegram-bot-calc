import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Путь к файлу и папке для сохранения изображений
excel_file_path = r'E:\TerminusFoto\FOTO300.xlsx'
output_folder = r'E:\TerminusFoto\Foto'

# Создаем папку, если она не существует
os.makedirs(output_folder, exist_ok=True)

# Читаем файл Excel
df = pd.read_excel(excel_file_path)

# Выводим структуру DataFrame для отладки
print(df.head())  # Вывод первых 5 строк DataFrame

# Проверяем, сколько столбцов у нас в DataFrame
num_columns = df.shape[1]
print(f"Количество столбцов: {num_columns}")

# Обрабатываем каждую строку в DataFrame
for index, row in df.iterrows():
    # Проверяем, есть ли значение в первом столбце (по имени столбца)
    first_column_name = df.columns[0]  # Получаем имя первого столбца
    if pd.isna(row[first_column_name]):
        break  # Если ячейка пустая, выходим из цикла
    
    # Запоминаем значение из первого столбца, убираем дробную часть
    base_name = str(int(row[first_column_name]))  # Преобразуем в int и обратно в str

    # Обрабатываем ссылки из столбцов 2-5, если они существуют
    for col_index in range(1, num_columns):  # Используем количество столбцов
        link = row.iloc[col_index]  # Используем iloc для доступа по индексу
        if pd.isna(link):
            continue  # Если ячейка пустая, переходим к следующему столбцу
        
        # Получаем HTML-страницу по ссылке
        response = requests.get(link)
        
        # Проверяем успешность запроса
        if response.status_code != 200:
            print(f"Ошибка при загрузке {link}: {response.status_code}")
            continue
        
        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем блок с изображениями
        image_div = soup.find('div', class_='bx-shared-preview-images')
        if image_div:
            img_tag = image_div.find('img')
            if img_tag:
                img_src = img_tag['src']
                # Формируем полную ссылку на изображение
                img_url = f"https://bitrix24public.com/{img_src}"
                
                
                # Определяем имя файла в зависимости от столбца
                file_name = f"{base_name}.png" if col_index == 1 else f"{base_name}-схема.png" if col_index == 2 else f"{base_name}-интерьер.png" if col_index == 3 else f"{base_name}-интерьер1.png" if col_index == 4 else f"{base_name}-интерьер2.png"

                # Скачиваем изображение
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    # Сохраняем изображение
                    with open(os.path.join(output_folder, file_name), 'wb') as f:
                        f.write(img_response.content)
                    print(f"Сохранено: {file_name}")
                    # print("Задержка")
                    # time.sleep(5)  # Задержка на 5 секунд
                    # print("Продолжаю")


                else:
                    print(f"Ошибка при загрузке изображения {img_url}: {img_response.status_code}")
        else:
            print(f"Не найден блок с изображениями на {link}")
