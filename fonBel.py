import os
from PIL import Image

# Папки с изображениями
print('Внимание!!!!!!!!!! Эта программа меняет фон фото!')
input_folder = input('Папка откуда берем фото')
output_folder = input('Папка куда берем фото - она должна быть другой!!!!!!!!!')

# Создаем выходную папку, если её нет
os.makedirs(output_folder, exist_ok=True)

# Проходим по всем файлам в папке
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.png'):
        try:
            # Полный путь к PNG файлу
            png_path = os.path.join(input_folder, filename)
            
            # Открываем PNG изображение
            png_image = Image.open(png_path).convert("RGBA")
            
            # Создаем белый фон 1000x1000
            background = Image.new("RGBA", (1050, 1050), (255, 255, 255, 255))
            
            # Вычисляем позицию для центрирования PNG изображения
            x = (background.width - png_image.width) // 2
            y = (background.height - png_image.height) // 2
            
            # Накладываем PNG изображение на фон
            background.paste(png_image, (x, y), png_image)  # Используем альфа-канал
            
            # Преобразуем изображение в RGB и сохраняем в JPG
            jpg_image = background.convert("RGB")
            
            # Формируем имя для сохранения
            jpg_filename = os.path.splitext(filename)[0] + '.jpg'
            jpg_path = os.path.join(output_folder, jpg_filename)
            
            # Сохраняем изображение в JPG
            jpg_image.save(jpg_path, 'JPEG')
        
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")

print("Конвертация завершена.")
