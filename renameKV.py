import os
# Укажите путь к папке
adress = input('введи адрес!')
# Укажите путь к папке
folder_path = adress

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    # Формируем полный путь к файлу
    old_file_path = os.path.join(folder_path, filename)
    
    # Проверяем, что это файл (а не папка)
    if os.path.isfile(old_file_path):
        # Создаем новое имя файла с префиксом "KV"
        new_filename = "KV" + filename
        new_file_path = os.path.join(folder_path, new_filename)
        
        # Переименовываем файл
        os.rename(old_file_path, new_file_path)

print("Префикс 'KV' добавлен ко всем файлам.")
