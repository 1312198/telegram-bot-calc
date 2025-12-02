import os

# Укажите путь к папке
folder_path = r"E:\Фоточки — копия"

# Проходим по всем файлам в указанной папке
for filename in os.listdir(folder_path):
    # Проверяем, содержится ли '-' в имени файла
    if '_' in filename:
        # Создаем новое имя файла с заменой
        new_filename = filename.replace('_', '-com_')
        # Полные пути к старому и новому файлам
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        # Переименовываем файл
        os.rename(old_file, new_file)
        print(f"Переименован: {old_file} -> {new_file}")

print("Замена завершена!")
