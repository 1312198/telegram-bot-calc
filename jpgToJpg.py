import os
import subprocess
import time

# Путь к папке с изображениями
folder_path = r'E:\ТД Рустрейд\Контент\Velvex\Фото\Зеркальные шкафы'

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.bmp', '.gif', '.jpeg', '.jpg')):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)

        # Открываем файл в Paint
        subprocess.Popen(['mspaint', file_path])

        # Ждем немного, чтобы Paint успел открыться
        time.sleep(1)

print("Все изображения открыты в Paint!")
