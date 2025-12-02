import os
from PIL import Image

# Указываем путь к папке
folder_path = r'C:\Users\Михаил\Downloads\Фото Хофф 2005\Hoff итога 20 мая фото'

# Перебираем все файлы в папке
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Проверяем, что файл является изображением
        img_path = os.path.join(folder_path, filename)
        image = Image.open(img_path)

        # Вычисляем ширину и высоту изображения
        width, height = image.size

        # Проверяем, нужно ли увеличивать изображение
        if width < 1000 and height < 1000:
            # Рассчитываем коэффициент увеличения
            scale_factor = 1000 / min(width, height)

            # Пропорционально увеличиваем изображение
            image = image.resize((int(width * scale_factor), int(height * scale_factor)))

        # Сохраняем результат вместо исходного изображения
        image.save(img_path, image.format)
