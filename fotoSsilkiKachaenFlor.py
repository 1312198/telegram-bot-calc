import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os

def download_and_convert_image(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Создаем объект изображения
        img = Image.open(BytesIO(response.content))
        
        # Конвертируем в JPG и сохраняем
        img.convert('RGB').save(output_path, 'JPEG', quality=95)
        
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")

def main():
    try:
        # Получаем путь к файлу и номер последней строки
        excel_path = input("Введите путь к Excel файлу: ")
        max_row = int(input("До какой строки обрабатывать данные? "))
        
        # Читаем Excel файл
        df = pd.read_excel(excel_path)
        
        # Проверяем существование папки для сохранения
        save_folder = 'E:\\Флорентина фото'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
            
        # Проходим по строкам
        for index, row in df.iloc[:max_row].iterrows():
            # Проверяем наличие данных в первом столбце
            if pd.notna(row[0]):
                name = row[0]
                
                # Обрабатываем изображения из каждого столбца
                for col_num, suffix in zip(range(1, 4), ["", "-схема", "-интерьер"]):
                    if pd.notna(row[col_num]):
                        url = row[col_num]
                        file_name = f"{name}{suffix}.jpg"
                        file_path = os.path.join(save_folder, file_name)
                        
                        download_and_convert_image(url, file_path)
                        print(f"Изображение сохранено: {file_path}")
            else:
                print(f"Пропущена строка {index+1}: нет данных в первом столбце")
                
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
