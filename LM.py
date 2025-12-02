import os

# Указываем путь к папке
folder_path = input("Дима, тупое днище. Сюда нужно вставить... Твое очко и Ванькин член! Что бы вас обоих собаки обосрали. Эта ебучая программа вообще не хотела рабоать! Я ее рот ебал! В общем - вставь адрес папки! По всем вопросам связанным с багами - ИДИТЕ НА ХУЙ!________:")

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    # Полный путь к файлу
    old_file_path = os.path.join(folder_path, filename)
    
    # Проверяем, что это файл (а не папка)
    if os.path.isfile(old_file_path):
        # Создаем новое имя файла
        new_filename = f"{os.path.splitext(filename)[0]}-LM{os.path.splitext(filename)[1]}"
        new_file_path = os.path.join(folder_path, new_filename)
        
        # Переименовываем файл
        os.rename(old_file_path, new_file_path)
        print(f"Переименован: {old_file_path} -> {new_file_path}")
