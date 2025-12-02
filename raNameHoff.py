import os

# Укажите путь к папке
folder_path = input('Введите адрес папки для сохранения')

# Создаем словарь замен
replacements = {
    "-схема.jpg": "_1.jpg",
    "-интерьер.jpg": "_2.jpg",
    "-интерьер1.jpg": "_3.jpg",
    "-интерьер2.jpg": "_4.jpg",
    "-интерьер3.jpg": "_5.jpg",
    "-интерьер4.jpg": "_6.jpg",
    "-интерьер5.jpg": "_7.jpg",
    "-интерьер6.jpg": "_8.jpg",
    "-интерьер7.jpg": "_9.jpg",
    "-интерьер8.jpg": "_10.jpg",
    "-интерьер10.jpg": "_11.jpg",
    "-интерьер11.jpg": "_12.jpg",
    "-интерьер12.jpg": "_13.jpg",
    "-интерьер13.jpg": "_14.jpg"

}

# Проходим по всем файлам в указанной папке
for filename in os.listdir(folder_path):
    new_filename = filename
    # Заменяем части названия
    for old, new in replacements.items():
        new_filename = new_filename.replace(old, new)
    
    # Если новое имя отличается от старого, переименовываем файл
    if new_filename != filename:
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        os.rename(old_file_path, new_file_path)
        print(f"Переименован: '{filename}' -> '{new_filename}'")
