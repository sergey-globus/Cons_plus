from django.db import models
from django.contrib.auth.models import User
import json
from .crypto import GOSTCrypto

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


from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .crypto import GOSTCrypto

class Consultation(models.Model):
    """
    Модель для хранения заявок на консультацию с автоматическим шифрованием персональных данных
    """
    _first_name = models.CharField(
        max_length=255, 
        verbose_name="Имя (зашифровано)",
        db_column='first_name'
    )
    _last_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия (зашифровано)",
        db_column='last_name'
    )
    _email = models.CharField(
        max_length=255,
        verbose_name="Email (зашифровано)",
        db_column='email'
    )
    
    question = models.TextField(verbose_name="Вопрос")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультации"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{self.id} от {self.created_at.strftime('%d.%m.%Y')}"

    @property
    def first_name(self):
        """Возвращает расшифрованное имя"""
        try:
            return GOSTCrypto().decrypt(self._first_name)
        except Exception as e:
            return f"Ошибка дешифровки: {str(e)}"

    @first_name.setter
    def first_name(self, value):
        """Шифрует и сохраняет имя"""
        if not isinstance(value, str):
            raise ValidationError("Имя должно быть строкой")
        self._first_name = GOSTCrypto().encrypt(value)

    @property
    def last_name(self):
        """Возвращает расшифрованную фамилию"""
        try:
            return GOSTCrypto().decrypt(self._last_name)
        except Exception as e:
            return f"Ошибка дешифровки: {str(e)}"

    @last_name.setter
    def last_name(self, value):
        """Шифрует и сохраняет фамилию"""
        if not isinstance(value, str):
            raise ValidationError("Фамилия должна быть строкой")
        self._last_name = GOSTCrypto().encrypt(value)

    @property
    def email(self):
        """Возвращает расшифрованный email"""
        try:
            return GOSTCrypto().decrypt(self._email)
        except Exception as e:
            return f"Ошибка дешифровки: {str(e)}"

    @email.setter
    def email(self, value):
        """Шифрует и сохраняет email"""
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError("Некорректный email адрес")
        self._email = GOSTCrypto().encrypt(value)

    def get_decrypted_data(self):
        """Возвращает все расшифрованные данные в виде словаря"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'question': self.question,
            'created_at': self.created_at
        }

    def send_notification(self):
        """Метод для отправки уведомления клиенту"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            send_mail(
                subject='Ваша заявка принята',
                message=f'Уважаемый(ая) {self.first_name} {self.last_name}, ваша заявка получена!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            return False

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

    def get_translated_fields(self):
        """Возвращает переведенные поля только для используемых в этом шаблоне"""
        FIELD_TRANSLATIONS = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'passport_number': 'Номер паспорта',
            'phone': 'Телефон',
            'email': 'Email',
            'date': 'Дата',
            'order_number': 'Номер заказа',
            'address': 'Адрес',
            'seller_name': 'Наименование продавца',
            'product_name': 'Наименование товара',
            'product_price': 'Стоимость товара',
            'product_article': 'Артикул товара',
            'purchase_date': 'Дата покупки',
            'order_amount': 'Сумма заказа',
            'date_order': 'Дата заказа',
            'return_reason': 'Причина возврата',
            'violation_description': 'Описание нарушения',
            'demands': 'Ваши требования'
        }
        
        return [
            {'eng_name': field, 'rus_name': FIELD_TRANSLATIONS.get(field, field)}
            for field in self.required_fields
        ]
    
class ArticleCategory(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Article(models.Model):
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title