"""
API модуль для Wildberries
"""
import time
import requests
from typing import List, Dict, Optional
from utils import logger


class WBAPI:
    """Класс для работы с API Wildberries"""
    
    BASE_URL = "https://suppliers-api.wildberries.ru"
    
    def __init__(self, api_key: str):
        """
        Инициализация API
        
        Args:
            api_key: API ключ Wildberries
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": api_key,
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, url: str, data: dict = None,
                      retries: int = 3, delay: float = 1.0) -> Optional[dict]:
        """
        Выполнение запроса к API
        
        Args:
            method: HTTP метод
            url: URL запроса
            data: данные для отправки
            retries: количество попыток
            delay: задержка между попытками
        
        Returns:
            dict: ответ от API или None при ошибке
        """
        for attempt in range(retries):
            try:
                if method.upper() == "POST":
                    response = self.session.post(url, json=data)
                else:
                    response = self.session.get(url, params=data)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    logger.error("WB API: Ошибка авторизации. Проверьте API ключ")
                    return {"error": "unauthorized", "details": "Invalid API key"}
                elif response.status_code == 403:
                    logger.warning(f"WB API: Получен 403, попытка {attempt + 1}/{retries}")
                    if attempt < retries - 1:
                        time.sleep(delay * (attempt + 1))
                        continue
                    return {"error": "forbidden", "details": response.text}
                else:
                    logger.error(f"WB API: Ошибка {response.status_code}: {response.text}")
                    return {"error": response.status_code, "details": response.text}
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"WB API: Исключение при запросе: {e}")
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))
                    continue
                return {"error": "exception", "details": str(e)}
        
        return {"error": "max_retries"}
    
    def get_feedbacks(self, is_answered: bool = None, limit: int = 1000) -> List[Dict]:
        """
        Получение отзывов
        
        Args:
            is_answered: фильтр по отвеченным (None - все)
            limit: количество отзывов
        
        Returns:
            List[Dict]: список отзывов
        """
        url = f"{self.BASE_URL}/api/v1/supplier/feedbacks"
        params = {
            "limit": limit
        }
        
        result = self._make_request("GET", url, params)
        
        if result is None:
            logger.error("WB API: Получен пустой ответ от API")
            return []
        
        if "error" in result:
            logger.error(f"WB API: Ошибка при получении отзывов: {result}")
            return []
        
        feedbacks = result.get("data", [])
        
        # Фильтрация по answered
        if is_answered is not None:
            feedbacks = [f for f in feedbacks if f.get("is_answered") == is_answered]
        
        return feedbacks
    
    def get_unanswered_feedbacks(self, limit: int = 1000) -> List[Dict]:
        """
        Получение неотвеченных отзывов
        
        Args:
            limit: количество отзывов
        
        Returns:
            List[Dict]: неотвеченные отзывы
        """
        feedbacks = self.get_feedbacks(is_answered=False, limit=limit)
        
        logger.info(f"WB API: Найдено {len(feedbacks)} неотвеченных отзывов")
        return feedbacks
    
    def send_answer(self, feedback_id: str, text: str) -> bool:
        """
        Отправка ответа на отзыв
        
        Args:
            feedback_id: ID отзыва
            text: текст ответа
        
        Returns:
            bool: успешность отправки
        """
        url = f"{self.BASE_URL}/api/v1/supplier/feedbacks/{feedback_id}/answer"
        data = {
            "answer": text
        }
        
        result = self._make_request("POST", url, data)
        
        if result is not None and "error" not in result:
            logger.info(f"WB API: Ответ отправлен на отзыв {feedback_id}")
            return True
        
        logger.error(f"WB API: Не удалось отправить ответ на отзыв {feedback_id}: {result}")
        return False


class WBMacrosAPI:
    """Класс для работы с API Wildberries через Macros (альтернативный метод)"""
    
    BASE_URL = "https://wildberries.ru"
    
    def __init__(self, api_key: str):
        """
        Инициализация API
        
        Args:
            api_key: API ключ Wildberries
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": api_key,
            "Content-Type": "application/json"
        })
    
    def get_orders(self, date_start: str = None, date_end: str = None, limit: int = 100) -> List[Dict]:
        """
        Получение заказов
        
        Args:
            date_start: начальная дата
            date_end: конечная дата
            limit: количество заказов
        
        Returns:
            List[Dict]: список заказов
        """
        url = f"{self.BASE_URL}/api/v1/orders"
        params = {
            "limit": limit
        }
        if date_start:
            params["date_start"] = date_start
        if date_end:
            params["date_end"] = date_end
        
        result = self._make_request("GET", url, params)
        
        if result is not None and "error" not in result:
            return result.get("orders", [])
        
        return []
    
    def _make_request(self, method: str, url: str, data: dict = None,
                      retries: int = 3, delay: float = 1.0) -> Optional[dict]:
        """Выполнение запроса к API"""
        for attempt in range(retries):
            try:
                if method.upper() == "POST":
                    response = self.session.post(url, json=data)
                else:
                    response = self.session.get(url, params=data)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"WB Macros API: Ошибка {response.status_code}: {response.text}")
                    return {"error": response.status_code, "details": response.text}
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"WB Macros API: Исключение: {e}")
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))
                    continue
        
        return {"error": "max_retries"}

