import os
from PIL import Image

# Укажите пути к папкам
print('Внимание!!!!!!!!!! Эта программа меняет размер фото под 1200 пикселей с одной стороны!')
input_folder = input('Папка откуда берем фото')
output_folder = input('Папка куда берем фото - она должна быть другой!!!!!!!!!')

# Создаем выходную папку, если ее нет
os.makedirs(output_folder, exist_ok=True)

# Проходим по всем файлам в папке с изображениями
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Проверяем, что это изображение
        img_path = os.path.join(input_folder, filename)
        try:    
            with Image.open(img_path) as img:
                width, height = img.size
                
                if width == height:  # Если изображение квадратное
                    new_size = (1000, 1000)
                else:  # Если изображение прямоугольное
                    if width > height:
                        new_width = 1000
                        new_height = int((height / width) * new_width)
                    else:
                        new_height = 1000
                        new_width = int((width / height) * new_height)
                    new_size = (new_width, new_height)
                
                # Изменяем размер изображения
                resized_img = img.resize(new_size, Image.ANTIALIAS)
                
                # Сохраняем измененное изображение в выходную папку
                resized_img.save(os.path.join(output_folder, filename))
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

print("Изображения успешно изменены и сохранены.")


