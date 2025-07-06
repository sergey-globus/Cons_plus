from django.db import models
from django.contrib.auth.models import User
import json

class FAQ(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    category = models.CharField(max_length=100, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"

    def __str__(self):
        return self.title

class Consultation(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    question = models.TextField(verbose_name="Вопрос")
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультации"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class DocumentTemplate(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название шаблона")
    template_content = models.TextField(verbose_name="Содержание шаблона")
    required_fields_json = models.TextField(default='[]', verbose_name="Обязательные поля")

    class Meta:
        verbose_name = "Шаблон документа"
        verbose_name_plural = "Шаблоны документов"

    def __str__(self):
        return self.name
    
    @property
    def required_fields(self):
        """Получить список обязательных полей"""
        try:
            return json.loads(self.required_fields_json)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_required_fields(self, fields_list):
        """Установить список обязательных полей"""
        self.required_fields_json = json.dumps(fields_list)
