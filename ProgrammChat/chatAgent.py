"""
Модуль для работы с чат-ботом и интеграции с API Ozon.

Этот модуль демонстрирует использование модуля ozon_api для получения 
информации о новых заказах и их обработки.
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict

# Импорт нашего модуля для работы с API Ozon
from ProgrammChat.ozon_api import OzonAPI, format_order_info


def process_new_orders(hours_ago: int = 24) -> List[Dict]:
    """
    Получение и обработка новых заказов.
    
    Args:
        hours_ago (int): За сколько последних часов получать заказы (по умолчанию 24)
        
    Returns:
        list: Список новых заказов
        
    Example:
        >>> orders = process_new_orders(48)
        >>> print(f"Обработано {len(orders)} заказов")
    """
    try:
        # Создание экземпляра API (параметры берутся из переменных окружения)
        api = OzonAPI()
        
        # Получение новых заказов
        orders = api.get_new_orders(hours_ago=hours_ago)
        
        # Обработка каждого заказа
        processed_orders = []
        for order in orders:
            # Здесь можно добавить дополнительную обработку заказа
            # Например, сохранение в базу данных, отправка уведомлений и т.д.
            
            # Форматирование информации о заказе
            order_info = {
                "order_id": order.get("order_id"),
                "created_at": order.get("created_at"),
                "status": order.get("status"),
                "products_count": len(order.get("products", [])),
                "total_amount": order.get("financial_data", {}).get("total_amount", 0)
            }
            
            processed_orders.append(order_info)
        
        return processed_orders
        
    except Exception as e:
        print(f"Ошибка при обработке заказов: {e}")
        raise


def display_orders_summary(orders: List[Dict]) -> None:
    """
    Отображение сводной информации о заказах.
    
    Args:
        orders (list): Список заказов для отображения
    """
    if not orders:
        print("Новых заказов не найдено")
        return
    
    print(f"Найдено {len(orders)} новых заказов:")
    print("=" * 50)
    
    total_amount = 0
    total_products = 0
    
    for i, order in enumerate(orders, 1):
        print(f"{i}. Заказ №{order['order_id']}")
        print(f"   Создан: {order['created_at']}")
        print(f"   Статус: {order['status']}")
        print(f"   Товаров: {order['products_count']}")
        print(f"   Сумма: {order['total_amount']}")
        print()
        
        total_amount += order['total_amount'] or 0
        total_products += order['products_count']
    
    print("=" * 50)
    print(f"ИТОГО:")
    print(f"  Заказов: {len(orders)}")
    print(f"  Товаров: {total_products}")
    print(f"  Сумма: {total_amount}")


def main():
    """
    Основная функция для демонстрации работы с API Ozon.
    
    Перед запуском необходимо установить переменные окружения:
    - OZON_CLIENT_ID - Client-Id из личного кабинета продавца Ozon
    - OZON_API_KEY - Api-Key из личного кабинета продавца Ozon
    
    Пример установки переменных окружения в Windows:
        set OZON_CLIENT_ID=ваш_client_id
        set OZON_API_KEY=ваш_api_key
        
    Пример установки переменных окружения в Linux/Mac:
        export OZON_CLIENT_ID=ваш_client_id
        export OZON_API_KEY=ваш_api_key
    """
    print("Демонстрация работы с API Ozon")
    print("=" * 40)
    
    try:
        # Получение новых заказов за последние 24 часа
        print("Получение новых заказов за последние 24 часа...")
        orders = process_new_orders(hours_ago=24)
        
        # Отображение сводной информации
        display_orders_summary(orders)
        
        # Демонстрация получения всех заказов (с пагинацией)
        print("\nПолучение всех новых заказов...")
        api = OzonAPI()
        all_orders = api.get_all_new_orders(hours_ago=24)
        print(f"Всего новых заказов: {len(all_orders)}")
        
        # Если есть заказы, показать детали первого
        if all_orders:
            first_order = all_orders[0]
            print(f"\nДетали первого заказа (№{first_order['order_id']}):")
            print(format_order_info(first_order))
            
            # Получение полной информации о заказе
            print("\nПолучение полной информации о заказе...")
            order_details = api.get_order_details(first_order['order_id'])
            print("Полная информация получена успешно")
            
    except ValueError as e:
        print(f"\nОшибка конфигурации: {e}")
        print("Убедитесь, что установлены переменные окружения OZON_CLIENT_ID и OZON_API_KEY")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Проверьте подключение к интернету и корректность данных доступа к API")


# Точка входа в программу
if __name__ == "__main__":
    main()