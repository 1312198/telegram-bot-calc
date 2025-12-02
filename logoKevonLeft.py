import os
from PIL import Image

# Папки с изображениями
source_folder = r"C:\Users\Михаил\Desktop\Фото Kevon\В работе\1\Лево"
overlay_image_path = r"C:\Users\Михаил\Desktop\Фото Kevon\В работе\Kevon by Haiba.png"

# Загружаем изображение, которое будем накладывать
overlay_image = Image.open(overlay_image_path)

# Проходим по всем файлам в папке
for filename in os.listdir(source_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Проверяем, является ли файл изображением
        # Полный путь к изображению
        image_path = os.path.join(source_folder, filename)

        # Загружаем основное изображение
        base_image = Image.open(image_path)

        # Получаем размеры изображений
        base_width, base_height = base_image.size
        overlay_width, overlay_height = overlay_image.size

        # Вычисляем позицию для наложения (левый нижний угол)
        position = (0, base_height - overlay_height)

        # Накладываем изображение
        base_image.paste(overlay_image, position, overlay_image.convert("RGBA"))

        # Сохраняем измененное изображение
        base_image.save(image_path)

print("Все изображения успешно обработаны.")
