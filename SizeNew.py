import os
from PIL import Image

print('Внимание!!!!!!!!!! Программа изменяет размер фото до 970px и меняет фон!')
input_folder = input('Папка откуда берем фото: ')
output_folder = input('Папка куда сохраняем фото (должна быть другой!): ')

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    try:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(input_folder, filename)
            
            # Открываем изображение
            with Image.open(file_path) as img:
                # Конвертируем в RGBA для дальнейшей обработки
                img = img.convert("RGBA")
                
                # Получаем исходные размеры
                width, height = img.size
                
                # Определяем новый размер
                if width == height:  # Квадратное
                    new_size = (970, 970)
                else:  # Прямоугольное
                    if width > height:
                        new_width = 970
                        new_height = int((height / width) * new_width)
                    else:
                        new_height = 970
                        new_width = int((width / height) * new_height)
                    new_size = (new_width, new_height)
                
                # Изменяем размер
                resized_img = img.resize(new_size, Image.ANTIALIAS)
                
                # Создаем белый фон
                background = Image.new("RGBA", (1000, 1000), (255, 255, 255, 255))
                
                # Вычисляем позицию для центрирования
                x = (background.width - resized_img.width) // 2
                y = (background.height - resized_img.height) // 2
                
                # Накладываем изображение на фон
                background.paste(resized_img, (x, y), resized_img)
                
                # Конвертируем в RGB для сохранения в JPG
                final_img = background.convert("RGB")
                
                # Формируем имя файла
                new_filename = os.path.splitext(filename)[0] + '.jpg'
                save_path = os.path.join(output_folder, new_filename)
                
                # Сохраняем результат
                final_img.save(save_path, 'JPEG')
                
    except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")

print("Обработка изображений завершена.")
