import openpyxl
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.hyperlink import Hyperlink

def process_excel_file(file_path):
    # Открываем файл
    wb = openpyxl.load_workbook(file_path)
    
    # Проходим по всем листам
    for sheet in wb.worksheets:
        # Проходим по всем ячейкам
        for row in sheet.iter_rows():
            for cell in row:
                # Проверяем наличие гиперссылки
                if cell.hyperlink:
                    try:
                        # Заменяем гиперссылку на её адрес
                        cell.value = cell.hyperlink.target
                        cell.hyperlink = None
                    except AttributeError:
                        # Обработка случая, если гиперссылка некорректна
                        print(f"Ошибка при обработке ячейки {cell.coordinate}")
    
    # Сохраняем изменения
    wb.save(file_path)
    print(f"Файл успешно обработан: {file_path}")

def main():
    # Запрашиваем путь к файлу
    file_path = input("Введите путь к Excel файлу: ")
    
    try:
        process_excel_file(file_path)
    except FileNotFoundError:
        print("Файл не найден. Проверьте путь к файлу.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
