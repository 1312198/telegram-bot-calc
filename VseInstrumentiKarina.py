import os
from PIL import Image

def resize_images(input_folder, output_folder):
    """Изменяет размер изображений до 1000 пикселей по большей стороне"""
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_folder, filename)
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    
                    if width == height:  # Квадратное изображение
                        new_size = (1000, 1000)
                    else:  # Прямоугольное изображение
                        if width > height:
                            new_width = 1000
                            new_height = int((height / width) * new_width)
                        else:
                            new_height = 1000
                            new_width = int((width / height) * new_height)
                        new_size = (new_width, new_height)
                    
                    resized_img = img.resize(new_size, Image.ANTIALIAS)
                    resized_img.save(os.path.join(output_folder, filename))
            except Exception as e:
                print(f"Ошибка при изменении размера {filename}: {e}")

def add_white_background(input_folder, output_folder):
    """Добавляет белый фон 1000x1000 и конвертирует в JPG"""
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        try:
            file_path = os.path.join(input_folder, filename)
            
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image = Image.open(file_path).convert("RGBA")
                background = Image.new("RGBA", (1000, 1000), (255, 255, 255, 255))
                
                x = (background.width - image.width) // 2
                y = (background.height - image.height) // 2
                
                background.paste(image, (x, y), image)
                jpg_image = background.convert("RGB")
                
                jpg_filename = os.path.splitext(filename)[0] + '.jpg'
                jpg_path = os.path.join(output_folder, jpg_filename)
                
                jpg_image.save(jpg_path, 'JPEG')
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")

def rename_files(folder_path):
    """Переименовывает файлы согласно заданным правилам"""
    files = os.listdir(folder_path)
    
    for file_name in files:
        # Шаг 1: добавляем _1 к имени файла
        new_file_name = file_name.replace('.', '_1.')
        
        if 'схема_1' in new_file_name:
            # Шаг 2: заменяем схема_1 на _2
            new_file_name = new_file_name.replace('-схема_1', '_2')
        elif 'интерьер_1' in new_file_name:
            # Шаг 3: заменяем интерьер_1 на _3
            new_file_name = new_file_name.replace('-интерьер_1', '_3')
        elif 'интерьер' in new_file_name:
            # Шаги 4 и далее: заменяем интерьерX_1 на _X+3
            try:
                interier_num = int(new_file_name.split('_')[0].split('-интерьер')[-1])
                new_file_name = new_file_name.replace(f'-интерьер{interier_num}_1', f'_{interier_num + 3}')
            except (ValueError, IndexError):
                # Если не удалось извлечь число, оставляем как есть
                pass
        
        # Переименовываем файл
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_file_name)
        os.rename(old_path, new_path)

def main():
    print("Программа выполняет три операции:")
    print("1. Изменение размера изображений")
    print("2. Добавление белого фона и конвертация в JPG")
    print("3. Переименование файлов")
    
    input_folder = input('Папка с исходными фото: ')
    output_folder = input('Папка для сохранения результатов (должна отличаться от исходной): ')
    
    # Этап 1: Изменение размера
    print("\n1. Изменение размера изображений...")
    resize_images(input_folder, output_folder)
    
    # Этап 2: Добавление фона
    print("\n2. Добавление белого фона...")
    add_white_background(output_folder, output_folder)
    
    # Этап 3: Переименование
    print("\n3. Переименование файлов...")
    rename_files(output_folder)
    
    print("\nВсе операции завершены успешно!")

if __name__ == "__main__":
    main()
