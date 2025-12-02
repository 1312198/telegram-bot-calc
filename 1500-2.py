import os
from PIL import Image

# Указываем пути к папкам
input_folder = r"C:\Users\Михаил\Downloads\Hoff new"
output_folder = r"C:\Users\Михаил\Downloads\obrabotka"

# Создаем выходную папку, если она не существует
os.makedirs(output_folder, exist_ok=True)

# Проходим по всем файлам в папке
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Проверяем, что это изображение
        # Открываем изображение
        img_path = os.path.join(input_folder, filename)
        with Image.open(img_path) as img:
            # Получаем размеры изображения
            width, height = img.size
            
            # Уменьшаем высоту, если она больше 1000 пикселей
            if height > 1000:
                ratio = 1000 / height
                height = 1000
                width = int(width * ratio)

            # Уменьшаем ширину, если она больше 1500 пикселей
            if width > 1500:
                ratio = 1500 / width
                width = 1500
                height = int(height * ratio)

            # Создаем новый фон белого цвета
            new_img = Image.new("RGB", (1500, 1000), (255, 255, 255))
            
            # Помещаем изображение по центру фона
            new_img.paste(img.resize((width, height)), ((1500 - width) // 2, (1000 - height) // 2))
            
            # Сохраняем новое изображение
            new_img.save(os.path.join(output_folder, filename))

print("Обработка завершена!")
