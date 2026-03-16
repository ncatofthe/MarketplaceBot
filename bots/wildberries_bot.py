"""
Бот для Wildberries
"""
from api import WBAPI
from .base_bot import BaseBot
from utils import logger
from config import config


class WildberriesBot(BaseBot):
    """Бот для автоматического ответа на отзывы Wildberries"""
    
    def __init__(self):
        super().__init__()
        self.api = None
        self.api_key = ""
    
    def connect(self) -> bool:
        """Подключение к API Wildberries"""
        try:
            # Получение настроек из конфигурации
            wb_config = config.get("wildberries")
            
            if not wb_config:
                logger.error("Wildberries: Конфигурация не найдена")
                return False
            
            self.api_key = wb_config.get("api_key", "")
            
            if not self.api_key:
                logger.error("Wildberries: API ключ не настроен")
                return False
            
            # Создание экземпляра API
            self.api = WBAPI(self.api_key)
            
            # Тестовый запрос для проверки подключения
            test_result = self.api.get_feedbacks(limit=1)
            if not test_result:
                logger.error("Wildberries: Не удалось выполнить тестовый запрос к API")
                return False
            
            logger.info("Wildberries: Успешное подключение к API")
            return True
            
        except Exception as e:
            logger.exception(f"Wildberries: Ошибка при подключении к API: {e}")
            return False
    
    def get_unanswered_reviews(self):
        """Получение неотвеченных отзывов"""
        if not self.api:
            logger.error("Wildberries: API не инициализирован")
            return []
        
        try:
            feedbacks = self.api.get_unanswered_feedbacks(limit=1000)
            
            # Преобразование формата отзывов
            formatted_feedbacks = []
            for feedback in feedbacks:
                formatted_feedbacks.append({
                    "id": feedback.get("id"),
                    "feedback_id": feedback.get("id"),
                    "rating": feedback.get("rating", 0),
                    "text": feedback.get("text", ""),
                    "comment": feedback.get("text", ""),
                    "product_id": feedback.get("sku"),
                    "product_name": feedback.get("product_name", ""),
                    "is_answered": feedback.get("is_answered", False),
                    "answer": feedback.get("answer")
                })
            
            return formatted_feedbacks
            
        except Exception as e:
            logger.exception(f"Wildberries: Ошибка при получении отзывов: {e}")
            return []
    
    def send_answer(self, review_id: str, text: str) -> bool:
        """Отправка ответа на отзыв"""
        if not self.api:
            logger.error("Wildberries: API не инициализирован")
            return False
        
        try:
            return self.api.send_answer(review_id, text)
        except Exception as e:
            logger.exception(f"Wildberries: Ошибка при отправке ответа: {e}")
            return False
    
    def get_status(self):
        """Получение статуса бота"""
        base_status = super().get_status()
        base_status.update({
            "name": "Wildberries",
            "api_key_configured": bool(self.api_key)
        })
        return base_status

