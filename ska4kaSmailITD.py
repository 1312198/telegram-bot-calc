# 1. Импорты и настройка логгера
import os
import re
import requests
from io import BytesIO
from PIL import Image
import openpyxl
import logging
from datetime import datetime

logging.basicConfig(
    filename='download_errors.log', 
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. Функция создания рабочей папки
def create_working_folder():
    base_folder = input("Введите путь к основной папке: ").strip()
    
    if not os.path.exists(base_folder):
        raise FileNotFoundError(f"Папка {base_folder} не существует")
    
    # Проверяем права доступа к базовой папке
    check_folder_permissions(base_folder)
    
    current_time = datetime.now().strftime("%H-%M")
    work_folder = os.path.join(base_folder, f"Фото-{current_time}")
    os.makedirs(work_folder, exist_ok=True)
    print(f"Создана папка: {work_folder}")
    
    try:
        # Ищем Excel файлы в базовой папке
        all_files = os.listdir(base_folder)
        print(f"Найдено файлов в папке: {len(all_files)}")
        
        excel_files = [f for f in all_files 
                      if f.lower().endswith(('.xlsx', '.xls'))]
        
        if not excel_files:
            print("\nВНИМАНИЕ: Excel файл не найден в папке!")
            print("Список всех найденных файлов:")
            for file in all_files:
                print(f"- {file}")
            raise FileNotFoundError("Excel файл не найден в папке")
        
        excel_path = os.path.join(base_folder, excel_files[0])
        print(f"\nВыбранный Excel файл: {excel_files[0]}")
        
        return work_folder, excel_path
        
    except Exception as e:
        logging.error(f"Ошибка при работе с файлами: {str(e)}")
        print(f"Произошла ошибка при работе с файлами: {str(e)}")
        raise

# 3. Функция проверки URL и скачивания
def download_image(url, save_path):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        if 'drive.google.com' in url:
            handle_google_drive(url, save_path)
        elif 'disk.yandex.ru' in url:
            handle_yandex_disk(url, save_path)
        elif 'mail.ru' in url:
            handle_mail_ru(url, save_path)
        else:
            handle_other_urls(url, save_path)
            
    except Exception as e:
        logging.error(f"Ошибка при скачивании {url}: {str(e)}")
        print(f"Ошибка при скачивании {url}: {str(e)}")

# 4. Обработка Google Drive
def handle_google_drive(url, save_path):
    try:
        match = re.search(r'/d/(a-zA-Z0-9_-+)', url)
        if match:
            file_id = match.group(1)
            download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
            response = requests.get(download_url, timeout=30)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.convert('RGB').save(save_path, 'JPEG')
            else:
                logging.error(f"Google Drive ошибка: {response.status_code}")
        else:
            logging.error(f"Неверный URL Google Drive: {url}")
    except Exception as e:
        logging.error(f"Ошибка Google Drive: {str(e)}")

# 5. Обработка Яндекс.Диск
def handle_yandex_disk(url, save_path):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        download_url = response.url
        
        if 'download.yandex.ru' in download_url:
            response = requests.get(download_url, timeout=30)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.convert('RGB').save(save_path, 'JPEG')
    except Exception as e:
        logging.error(f"Ошибка Яндекс.Диск: {str(e)}")

# 6. Обработка Mail.ru
def handle_mail_ru(url, save_path):
    try:
        if '/public/' in url:
            url = url.replace('/public/', '/download/')
        elif '/cloud/' in url:
            url = url.replace('/cloud/', '/download/')
        
        response = requests.get(url, allow_redirects=True, timeout=30)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.convert('RGB').save(save_path, 'JPEG')
    except Exception as e:
        logging.error(f"Ошибка Mail.ru: {str(e)}")

# 7. Обработка остальных URL
def handle_other_urls(url, save_path):
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.convert('RGB').save(save_path, 'JPEG')
    except Exception as e:
        logging.error(f"Ошибка при скачивании с {url}: {str(e)}")


# 8. Функция обработки Excel файла
def process_excel(excel_path, work_folder):
    try:
        # Открываем Excel файл
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active
        
        # Проходим по всем строкам, начиная со второй (пропускаем заголовок)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row:  # Проверяем, что строка не пустая
                # Предполагаем, что URL находится в первом столбце
                url = row[0]
                # Второе поле - имя файла (если есть)
                filename = row[1] if len(row) > 1 else None
                
                if not url:
                    continue  # Пропускаем строки без URL
                
                # Формируем имя файла для сохранения
                if filename:
                    save_name = f"{filename}.jpg"
                else:
                    # Генерируем имя файла, если не указано
                    save_name = f"image_{datetime.now().strftime('%H%M%S')}.jpg"
                
                # Полный путь для сохранения
                save_path = os.path.join(work_folder, save_name)
                
                # Информируем пользователя о процессе скачивания
                print(f"Скачивание: {url} -> {save_name}")
                
                # Вызываем функцию скачивания
                download_image(url, save_path)
                
    except Exception as e:
        # Логируем и выводим ошибку
        logging.error(f"Ошибка обработки Excel файла: {str(e)}")
        print(f"Ошибка при обработке Excel файла: {str(e)}")


# 9. Функция проверки интернет-соединения
def check_internet_connection():
    try:
        # Отправляем HEAD-запрос к Google для проверки подключения
        response = requests.head('https://www.google.com', timeout=5)
        # Проверяем успешный статус ответа
        return response.status_code == 200
    except requests.RequestException:
        # Если произошла любая ошибка запроса, возвращаем False
        return False


# 10. Главная функция
def main():
    try:
        print("Запуск программы...")
        
        # Проверяем интернет-соединение
        if not check_internet_connection():
            print("Ошибка: Нет подключения к интернету")
            exit(1)
            
        # Получаем рабочую папку и Excel файл
        work_folder, excel_path = create_working_folder()
        
        # Обрабатываем Excel файл
        process_excel(excel_path, work_folder)
        
        print("\nВсе изображения успешно скачаны!")
        print(f"Результаты сохранены в папке: {work_folder}")
        
    except FileNotFoundError as fnf:
        logging.critical(f"Файл не найден: {str(fnf)}")
        print(f"\nОшибка: {str(fnf)}")
        
    except PermissionError as pe:
        logging.critical(f"Ошибка доступа: {str(pe)}")
        print(f"\nНет прав доступа: {str(pe)}")
        
    except Exception as e:
        logging.critical(f"Критическая ошибка: {str(e)}")
        print("\nПроизошла непредвиденная ошибка. Подробности в логе.")

# 11. Функция проверки прав доступа
def check_folder_permissions(folder_path):
    try:
        if not os.access(folder_path, os.R_OK):
            raise PermissionError(f"Нет прав на чтение папки {folder_path}")
        if not os.access(folder_path, os.W_OK):
            raise PermissionError(f"Нет прав на запись в папку {folder_path}")
    except Exception as e:
        logging.error(f"Ошибка проверки прав: {str(e)}")
        raise

# 11.5 Функция проверки прав доступа к папке
def check_folder_permissions(folder_path):
    try:
        # Проверяем права на чтение
        if not os.access(folder_path, os.R_OK):
            raise PermissionError(f"Нет прав на чтение папки {folder_path}")
            
        # Проверяем права на запись
        if not os.access(folder_path, os.W_OK):
            raise PermissionError(f"Нет прав на запись в папку {folder_path}")
            
    except Exception as e:
        logging.error(f"Ошибка проверки прав доступа: {str(e)}")
        raise

# 12. Вспомогательные функции
def get_valid_filename(filename):
    """Очищает имя файла от недопустимых символов"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)

def check_image_format(url):
    """Проверяет формат изображения по URL"""
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('content-type')
        if content_type:
            return content_type.startswith('image/')
    except:
        pass
    return False

# Точка входа в программу
if __name__ == "__main__":
    main()
