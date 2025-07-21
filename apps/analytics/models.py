from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PageVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    page_url = models.URLField(max_length=500, verbose_name="URL страницы")
    page_title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок страницы")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    user_agent = models.TextField(verbose_name="User Agent")
    referer = models.URLField(max_length=500, blank=True, null=True, verbose_name="Источник перехода")
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name="Ключ сессии")
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name="Время посещения")

    class Meta:
        verbose_name = "Посещение страницы"
        verbose_name_plural = "Посещения страниц"
        ordering = ['-visited_at']
        indexes = [
            models.Index(fields=['visited_at']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['user']),
            models.Index(fields=['page_url']),
        ]

    def __str__(self):
        user_info = self.user.username if self.user else f"Анонимный ({self.ip_address})"
        return f"{user_info} - {self.page_url} - {self.visited_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def is_authenticated_user(self):
        """Проверка, авторизован ли пользователь"""
        return self.user is not None

    @property
    def short_url(self):
        """Сокращенный URL для отображения"""
        if len(self.page_url) > 50:
            return self.page_url[:47] + "..."
        return self.page_url

class UserSession(models.Model):
    """Модель для отслеживания пользовательских сессий"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    session_key = models.CharField(max_length=40, unique=True, verbose_name="Ключ сессии")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    user_agent = models.TextField(verbose_name="User Agent")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Начало сессии")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Последняя активность")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Пользовательская сессия"
        verbose_name_plural = "Пользовательские сессии"
        ordering = ['-last_activity']

    def __str__(self):
        user_info = self.user.username if self.user else f"Анонимный ({self.ip_address})"
        return f"Сессия {user_info} - {self.started_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def duration(self):
        """Продолжительность сессии"""
        return self.last_activity - self.started_at

    def mark_inactive(self):
        """Пометить сессию как неактивную"""
        self.is_active = False
        self.save()

class PopularPage(models.Model):
    """Модель для кэширования популярных страниц"""
    page_url = models.URLField(max_length=500, unique=True, verbose_name="URL страницы")
    page_title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок страницы")
    visit_count = models.PositiveIntegerField(default=0, verbose_name="Количество посещений")
    unique_visitors = models.PositiveIntegerField(default=0, verbose_name="Уникальных посетителей")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    class Meta:
        verbose_name = "Популярная страница"
        verbose_name_plural = "Популярные страницы"
        ordering = ['-visit_count']

    def __str__(self):
        return f"{self.page_title or self.page_url} ({self.visit_count} посещений)"

    @classmethod
    def update_stats(cls):
        """Обновить статистику популярных страниц"""
        from django.db.models import Count
        
        # Получаем статистику за последние 30 дней
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        
        popular_pages = PageVisit.objects.filter(
            visited_at__gte=thirty_days_ago
        ).values('page_url', 'page_title').annotate(
            visit_count=Count('id'),
            unique_visitors=Count('ip_address', distinct=True)
        ).order_by('-visit_count')
        
        # Обновляем или создаем записи
        for page_data in popular_pages:
            cls.objects.update_or_create(
                page_url=page_data['page_url'],
                defaults={
                    'page_title': page_data['page_title'] or '',
                    'visit_count': page_data['visit_count'],
                    'unique_visitors': page_data['unique_visitors']
                }
            )
