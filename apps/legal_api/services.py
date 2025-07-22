import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class LegalNewsService:
    def __init__(self):
        self.api_key = settings.LEGAL_API_KEY
        self.base_url = "https://api.legal-news.com/v1"
        
    def get_news(self, limit=10):
        """Получение правовых новостей"""
        cache_key = f"legal_news_{limit}"
        cached_news = cache.get(cache_key)
        
        if cached_news:
            return cached_news
            
        try:
            response = requests.get(
                f"{self.base_url}/news",
                headers={'Authorization': f'Bearer {self.api_key}'},
                params={'limit': limit},
                timeout=10
            )
            
            if response.status_code == 200:
                news_data = response.json()
                # Кэшируем на 1 час
                cache.set(cache_key, news_data, 3600)
                return news_data
            else:
                logger.error(f"API error: {response.status_code}")
                return self._get_fallback_news()
                
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return self._get_fallback_news()
    
    def search_legal_info(self, query):
        """Поиск правовой информации"""
        try:
            response = requests.get(
                f"{self.base_url}/search",
                headers={'Authorization': f'Bearer {self.api_key}'},
                params={'q': query},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'results': []}
                
        except requests.RequestException:
            return {'results': []}
    
    def _get_fallback_news(self):
        """Резервные новости при недоступности API"""
        return {
            'articles': [
                {
                    'title': 'Изменения в Гражданском кодексе РФ',
                    'content': 'Вступили в силу новые изменения в ГК РФ...',
                    'published_at': '2025-07-01',
                    'source': 'Официальный источник'
                },
                {
                    'title': 'Новые правила регистрации недвижимости',
                    'content': 'Упрощена процедура регистрации права собственности...',
                    'published_at': '2025-06-28',
                    'source': 'Росреестр'
                }
            ]
        }
