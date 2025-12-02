import os
from PIL import Image

# Путь к папке с изображениями
folder_path = input('Адрес папки:_____')

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Проверяем, является ли файл изображением
        file_path = os.path.join(folder_path, filename)
        
        try:
            # Открываем изображение
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Проверяем высоту
                if height > 1000:
                    new_height = 1000
                    new_width = int((new_height / height) * width)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                
                if height < 1000:
                    new_height = 1000
                    new_width = int((new_height / height) * width)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                
                # # Проверяем ширину
                # if width > 1000:
                #     new_width = 1000
                #     new_height = int((new_width / width) * height)
                #     img = img.resize((new_width, new_height), Image.ANTIALIAS)
                
                # Сохраняем измененное изображение
                img.save(file_path)
        
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")

print("Обработка изображений завершена.")

