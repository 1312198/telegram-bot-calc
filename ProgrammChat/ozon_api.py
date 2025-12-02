"""
Модуль для работы с API Ozon.

Этот модуль предоставляет функции для подключения к API Ozon и получения 
информации о новых заказах.

Для работы модуля необходимо:
1. Получить Client-Id и Api-Key в личном кабинете продавца Ozon
2. Установить переменные окружения:
   - OZON_CLIENT_ID - Client-Id из личного кабинета
   - OZON_API_KEY - Api-Key из личного кабинета

Пример использования:
    from ozon_api import OzonAPI
    
    # Создание экземпляра API
    api = OzonAPI()
    
    # Получение новых заказов за последние 24 часа
    orders = api.get_new_orders(hours_ago=24)
    
    # Вывод информации о заказах
    for order in orders:
        print(f"Заказ №{order['order_id']}, создан: {order['created_at']}")
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OzonAPI:
    """
    Класс для работы с API Ozon.
    
    Основные функции:
    - Подключение к API с использованием Client-Id и Api-Key
    - Получение списка новых заказов
    - Получение детальной информации о заказах
    """
    
    def __init__(self, client_id: Optional[str] = None, api_key: Optional[str] = None):
        """
        Инициализация клиента API Ozon.
        
        Args:
            client_id (str, optional): Client-Id из личного кабинета продавца.
                Если не указан, берется из переменной окружения OZON_CLIENT_ID.
            api_key (str, optional): Api-Key из личного кабинета продавца.
                Если не указан, берется из переменной окружения OZON_API_KEY.
                
        Raises:
            ValueError: Если не указаны client_id или api_key.
        """
        # Получение Client-Id из параметра или переменной окружения
        self.client_id = client_id or os.getenv('OZON_CLIENT_ID')
        if not self.client_id:
            raise ValueError(
                "Не указан Client-Id. Укажите его как параметр или установите "
                "переменную окружения OZON_CLIENT_ID"
            )
        
        # Получение Api-Key из параметра или переменной окружения
        self.api_key = api_key or os.getenv('OZON_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Не указан Api-Key. Укажите его как параметр или установите "
                "переменную окружения OZON_API_KEY"
            )
        
        # Базовый URL API Ozon
        self.base_url = "https://api-seller.ozon.ru"
        
        # Заголовки для всех запросов
        self.headers = {
            "Client-Id": self.client_id,
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        logger.info("Инициализирован клиент API Ozon для Client-Id: %s", self.client_id)
    
    def _make_request(self, endpoint: str, method: str = "POST", data: Optional[Dict] = None) -> Dict:
        """
        Выполнение HTTP-запроса к API Ozon.
        
        Args:
            endpoint (str): Конечная точка API (без базового URL)
            method (str): HTTP-метод (по умолчанию "POST")
            data (dict, optional): Данные для отправки в теле запроса
            
        Returns:
            dict: Ответ от API в формате JSON
            
        Raises:
            requests.RequestException: При ошибках сети или HTTP
            ValueError: При ошибках в ответе API
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.debug("Выполнение %s запроса к %s", method, url)
            
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=data)
            else:
                response = requests.post(url, headers=self.headers, json=data)
            
            # Проверка статуса ответа
            response.raise_for_status()
            
            # Парсинг JSON ответа
            result = response.json()
            
            # Проверка на ошибки в ответе API
            if "error" in result:
                error_msg = result["error"]
                logger.error("Ошибка API Ozon: %s", error_msg)
                raise ValueError(f"Ошибка API Ozon: {error_msg}")
            
            logger.debug("Запрос выполнен успешно")
            return result
            
        except requests.RequestException as e:
            logger.error("Ошибка при выполнении запроса к API: %s", str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Ошибка при парсинге JSON ответа: %s", str(e))
            raise ValueError(f"Некорректный формат ответа от API: {str(e)}")
    
    def get_new_orders(self, hours_ago: int = 24, limit: int = 100) -> List[Dict]:
        """
        Получение списка новых заказов.
        
        Args:
            hours_ago (int): За сколько последних часов получать заказы (по умолчанию 24)
            limit (int): Максимальное количество заказов в ответе (по умолчанию 100)
            
        Returns:
            list: Список заказов в формате словарей
            
        Example:
            >>> api = OzonAPI()
            >>> orders = api.get_new_orders(hours_ago=48)
            >>> print(f"Получено {len(orders)} заказов")
        """
        # Вычисление даты, начиная с которой нужно получить заказы
        since_date = datetime.utcnow() - timedelta(hours=hours_ago)
        since_timestamp = int(since_date.timestamp())
        
        logger.info(
            "Получение новых заказов с %s (UTC), лимит: %d", 
            since_date.strftime("%Y-%m-%d %H:%M:%S"), 
            limit
        )
        
        # Параметры запроса
        payload = {
            "filter": {
                "since": since_timestamp,  # Время в секундах
                "status": " awaiting_deliver"  # Статус "ожидает отгрузки"
            },
            "limit": limit,
            "with": {
                "analytics_data": True,     # Включить аналитические данные
                "financial_data": True      # Включить финансовую информацию
            }
        }
        
        try:
            # Выполнение запроса к API
            response = self._make_request("/v1/orders/list", data=payload)
            
            # Извлечение списка заказов из ответа
            orders = response.get("result", {}).get("orders", [])
            
            logger.info("Получено %d заказов", len(orders))
            return orders
            
        except Exception as e:
            logger.error("Ошибка при получении заказов: %s", str(e))
            raise
    
    def get_order_details(self, order_id: str) -> Dict:
        """
        Получение детальной информации о заказе.
        
        Args:
            order_id (str): Идентификатор заказа
            
        Returns:
            dict: Детальная информация о заказе
            
        Example:
            >>> api = OzonAPI()
            >>> order_details = api.get_order_details("123456789")
            >>> print(f"Сумма заказа: {order_details['order_amount']}")
        """
        logger.info("Получение деталей заказа №%s", order_id)
        
        # Параметры запроса
        payload = {
            "order_id": order_id
        }
        
        try:
            # Выполнение запроса к API
            response = self._make_request("/v1/orders/info", data=payload)
            
            # Извлечение информации о заказе из ответа
            order_info = response.get("result", {})
            
            logger.info("Детали заказа №%s успешно получены", order_id)
            return order_info
            
        except Exception as e:
            logger.error("Ошибка при получении деталей заказа №%s: %s", order_id, str(e))
            raise
    
    def get_all_new_orders(self, hours_ago: int = 24) -> List[Dict]:
        """
        Получение всех новых заказов с обработкой пагинации.
        
        Args:
            hours_ago (int): За сколько последних часов получать заказы (по умолчанию 24)
            
        Returns:
            list: Список всех новых заказов
            
        Example:
            >>> api = OzonAPI()
            >>> all_orders = api.get_all_new_orders(hours_ago=24)
            >>> print(f"Всего получено: {len(all_orders)} заказов")
        """
        logger.info("Получение всех новых заказов за последние %d часов", hours_ago)
        
        all_orders = []
        last_order_id = 0
        limit = 100  # Максимальное количество заказов за один запрос
        
        while True:
            # Параметры запроса с учетом пагинации
            payload = {
                "filter": {
                    "since": int((datetime.utcnow() - timedelta(hours=hours_ago)).timestamp()),
                    "status": "awaiting_deliver",
                    "order_id_gt": last_order_id  # Получение заказов с ID больше этого
                },
                "limit": limit,
                "with": {
                    "analytics_data": True,
                    "financial_data": True
                }
            }
            
            try:
                # Выполнение запроса к API
                response = self._make_request("/v1/orders/list", data=payload)
                
                # Извлечение списка заказов из ответа
                orders = response.get("result", {}).get("orders", [])
                
                if not orders:
                    # Если заказов больше нет, завершаем цикл
                    break
                
                # Добавляем полученные заказы к общему списку
                all_orders.extend(orders)
                
                # Обновляем last_order_id для следующей итерации
                last_order_id = max(order["order_id"] for order in orders)
                
                logger.debug("Получено %d заказов, всего: %d", len(orders), len(all_orders))
                
                # Если получено меньше заказов, чем лимит, значит это последняя страница
                if len(orders) < limit:
                    break
                    
            except Exception as e:
                logger.error("Ошибка при получении всех заказов: %s", str(e))
                raise
        
        logger.info("Всего получено %d заказов", len(all_orders))
        return all_orders


def format_order_info(order: Dict) -> str:
    """
    Форматирование информации о заказе для вывода.
    
    Args:
        order (dict): Словарь с информацией о заказе
        
    Returns:
        str: Отформатированная строка с информацией о заказе
    """
    try:
        order_id = order.get("order_id", "N/A")
        created_at = order.get("created_at", "N/A")
        status = order.get("status", "N/A")
        
        # Получение суммы заказа из финансовых данных
        financial_data = order.get("financial_data", {})
        order_amount = financial_data.get("total_amount", "N/A")
        
        # Получение количества товаров
        products_count = len(order.get("products", []))
        
        return (
            f"Заказ №{order_id}\n"
            f"  Создан: {created_at}\n"
            f"  Статус: {status}\n"
            f"  Сумма: {order_amount}\n"
            f"  Товаров: {products_count}\n"
        )
    except Exception as e:
        logger.error("Ошибка при форматировании информации о заказе: %s", str(e))
        return f"Ошибка форматирования заказа: {str(e)}"


# Пример использования модуля
if __name__ == "__main__":
    """
    Пример использования модуля для получения новых заказов.
    
    Перед запуском необходимо:
    1. Установить переменные окружения:
       - OZON_CLIENT_ID - Client-Id из личного кабинета продавца
       - OZON_API_KEY - Api-Key из личного кабинета продавца
       
    Пример установки переменных окружения в Windows:
        set OZON_CLIENT_ID=ваш_client_id
        set OZON_API_KEY=ваш_api_key
        
    Пример установки переменных окружения в Linux/Mac:
        export OZON_CLIENT_ID=ваш_client_id
        export OZON_API_KEY=ваш_api_key
    """
    
    try:
        # Создание экземпляра API
        print("Создание клиента API Ozon...")
        api = OzonAPI()
        
        # Получение новых заказов за последние 24 часа
        print("Получение новых заказов за последние 24 часа...")
        orders = api.get_new_orders(hours_ago=24)
        
        if not orders:
            print("Новых заказов не найдено")
        else:
            print(f"Получено {len(orders)} заказов:")
            print("-" * 50)
            
            # Вывод информации о каждом заказе
            for i, order in enumerate(orders, 1):
                print(f"{i}. {format_order_info(order)}")
        
        # Получение всех новых заказов (с обработкой пагинации)
        print("\nПолучение всех новых заказов...")
        all_orders = api.get_all_new_orders(hours_ago=24)
        print(f"Всего новых заказов: {len(all_orders)}")
        
        # Получение детальной информации о первом заказе (если есть)
        if all_orders:
            first_order_id = all_orders[0]["order_id"]
            print(f"\nПолучение деталей заказа №{first_order_id}...")
            order_details = api.get_order_details(first_order_id)
            print("Детали заказа получены успешно")
            
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}")
        print("Убедитесь, что установлены переменные окружения OZON_CLIENT_ID и OZON_API_KEY")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print("Проверьте подключение к интернету и корректность данных доступа к API")