import os
from PIL import Image

# Указываем путь к папке
folder_path = r'C:\Users\Михаил\Downloads\Фото Хофф 2005\photo — копия'

# Перебираем все файлы в папке
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Проверяем, что файл является изображением
        img_path = os.path.join(folder_path, filename)
        image = Image.open(img_path)

        # Вычисляем ширину и высоту изображения
        width, height = image.size

        if height >= width:
            # Создаём белый фон в соотношении 3:2, где высота фона равна высоте изображения
            new_width = int(height * 1.5)  # Расчёт ширины для соотношения 3:2
            background = Image.new('RGB', (new_width, height), color=(255, 255, 255))

            # Помещаем изображение поверх фона по центру
            box = (int((new_width - width) / 2), 0)  # Координаты для размещения изображения по центру
            background.paste(image, box)
        else:
            # Создаём белый фон в соотношении 3:2, где ширина фона равна ширине изображения
            new_height = int(width * 2 / 3)  # Расчёт высоты для соотношения 3:2
            background = Image.new('RGB', (width, new_height), color=(255, 255, 255))

            # Помещаем изображение поверх фона по центру
            box = (0, int((new_height - height) / 2))  # Координаты для размещения изображения по центру
            background.paste(image, box)

        # Сохраняем результат вместо исходного изображения
        background.save(img_path, image.format)
