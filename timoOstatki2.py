import pandas as pd
from io import BytesIO
from ftplib import FTP
from datetime import datetime
import os

# Настройки FTP
ftp_server = 'ftp.timo.ru'
ftp_port = 12100
ftp_user = 'user1'
ftp_password = 'kbkenhrk.'

# Файлы для загрузки
file_path_1 = '/Dush/Остатки 1С.csv'
file_path_2 = '/smesiteli/Остатки 1С.csv'

# Подключение к FTP-серверу
ftp = FTP()
ftp.connect(ftp_server, ftp_port)

# Попытка входа
try:
    ftp.login(ftp_user, ftp_password)
except Exception as e:
    print(f'Ошибка входа на FTP: {e}')
    exit(1)

# Функция для загрузки CSV и преобразования в DataFrame
def load_csv_from_ftp(file_path):
    csv_data = BytesIO()
    ftp.retrbinary(f'RETR {file_path}', csv_data.write)
    csv_data.seek(0)  # Возврат в начало файла
    return pd.read_csv(csv_data, sep=';', on_bad_lines='warn')

# Чтение CSV и создание Excel
try:
    df1 = load_csv_from_ftp(file_path_1)
    df2 = load_csv_from_ftp(file_path_2)

    # Получение текущей даты и времени для имени файла
    current_time = datetime.now().strftime('%Y-%m-%d %H-%M')
    excel_file_name = f'Остатки TIMO {current_time}.xlsx'
    
    # Путь к рабочему столу
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    excel_file_path = os.path.join(desktop_path, excel_file_name)
    
    # Создание Excel-файла с двумя листами
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='Остатки 1С', index=False)
        df2.to_excel(writer, sheet_name='Остатки Smesiteli', index=False)

    print(f'Файл Excel сохранен как {excel_file_path}')
except Exception as e:
    print(f'Ошибка при чтении CSV: {e}')

# Закрытие соединения
ftp.quit()

input("Нажмите Enter, чтобы закрыть консоль...")
