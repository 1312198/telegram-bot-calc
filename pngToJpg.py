import os
from PIL import Image

# Укажите путь к вашей папке
folder_path = r"E:\ТД Рустрейд\Контент\Double You\Фото"

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        # Полный путь к файлу
        png_file_path = os.path.join(folder_path, filename)
        jpg_file_path = os.path.join(folder_path, filename[:-4] + ".jpg")

        # Открываем PNG файл и сохраняем его как JPG
        with Image.open(png_file_path) as img:
            img.convert("RGB").save(jpg_file_path, "JPEG")

        # Удаляем оригинальный PNG файл
        os.remove(png_file_path)

print("Преобразование завершено!")

