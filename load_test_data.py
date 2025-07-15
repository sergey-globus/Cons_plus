import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_portal.settings')
django.setup()

from apps.main.models import FAQ, DocumentTemplate

# FAQ.objects.all().delete()
# print("✓ Старые записи FAQ удалены")


def load_test_data():
    print("Загрузка тестовых данных...")

    # Создание FAQ
    faq_data = [
        {
            'title': 'Возврат товара надлежащего качества',
            'synonyms': 'сроки возврата товара, требования к возвращаемому товару, требования к товару, процедура возврата',
            'description': 'Сроки, требования и процедура возврата товаров, купленных на маркетплейсах',
            'tags': 'Возврат товаров,7 дней,Качество',
            'icon_class': 'fas fa-undo-alt',
            'url_name': 'marketplace_rights',
        },
        {
            'title': 'Отмена заказа продавцом',
            'synonyms': 'отказ продавцом, отмена покупки продавцом, права покупателя',
            'description': 'Что делать, если продавец или маркетплейс отменил ваш заказ в одностороннем порядке',
            'tags': 'Отмена заказа,Права покупателя,Компенсация',
            'icon_class': 'fas fa-times-circle',
            'url_name': 'order_cancellation',
        },
        {
            'title': 'Ошибочная цена товара',
            'synonyms': 'техническая ошибка в цене',
            'description': 'Может ли продавец отказаться от исполнения договора из-за технической ошибки в цене',
            'tags': 'Ошибка цены,Публичная оферта,Договор',
            'icon_class': 'fas fa-exclamation-triangle',
            'url_name': 'price_error',
        },
    ]

    for faq in faq_data:
        obj, created = FAQ.objects.get_or_create(
            title=faq['title'],
            defaults={
                'synonyms': faq['synonyms'],
                'description': faq['description'],
                'tags': faq['tags'],
                'icon_class': faq['icon_class'],
                'url_name': faq['url_name'],
            }
        )
        if created:
            print(f"✓ Создан FAQ: {faq['title']}")
        else:
            print(f"- FAQ уже существует: {faq['title']}")

    # Удаляем старые шаблоны
    DocumentTemplate.objects.all().delete()
    print("✓ Старые шаблоны удалены")

    # Создание новых шаблонов документов, связанных с маркетплейсами
    templates_data = [
        {
            'name': 'Претензия продавцу на маркетплейсе',
            'template_content': '''ПРЕТЕНЗИЯ

г. Москва                                                    {date}

Кому: {seller_name}
От кого: {last_name} {first_name} {middle_name}
Адрес: {address}
Телефон: {phone}
Email: {email}

ПРЕТЕНЗИЯ
о нарушении прав потребителя

Уважаемые коллеги!

{date_order} я оформил(а) заказ № {order_number} на маркетплейсе на сумму {order_amount} рублей.

Товар: {product_name}
Артикул: {product_article}

Однако Вы нарушили мои права как потребителя, а именно: {violation_description}

На основании статей 18, 23 Закона РФ "О защите прав потребителей" требую:
{demands}

В случае неудовлетворения данной претензии в течение 10 дней буду вынужден(а) обратиться в суд.

Приложения:
- Копия чека
- Скриншоты переписки
- Фотографии товара

Дата: {date}                    Подпись: ________________
                                {last_name} {first_name} {middle_name}''',
            'required_fields': ['date', 'seller_name', 'first_name', 'last_name', 'middle_name', 'address', 'phone', 'email', 'date_order', 'order_number', 'order_amount', 'product_name', 'product_article', 'violation_description', 'demands']
        },
        {
            'name': 'Заявление на возврат товара',
            'template_content': '''ЗАЯВЛЕНИЕ
на возврат товара надлежащего качества

г. Москва                                                    {date}

Продавцу: {seller_name}
От покупателя: {last_name} {first_name} {middle_name}
Паспорт: {passport_number}
Телефон: {phone}

ЗАЯВЛЕНИЕ

Прошу принять к возврату товар надлежащего качества, приобретенный {purchase_date} по заказу № {order_number}.

Наименование товара: {product_name}
Артикул: {product_article}
Стоимость: {product_price} рублей

Причина возврата: {return_reason}

Товар не был в употреблении, сохранены товарный вид, потребительские свойства, имеется чек.

На основании п. 4 ст. 26.1 Закона РФ "О защите прав потребителей" прошу:
1. Принять товар к возврату
2. Вернуть уплаченную сумму в размере {product_price} рублей в течение 10 дней

Приложения:
- Товар в оригинальной упаковке
- Копия чека/документа об оплате

Дата: {date}                    Подпись: ________________
                                {last_name} {first_name} {middle_name}''',
            'required_fields': ['date', 'seller_name', 'first_name', 'last_name', 'middle_name', 'passport_number', 'phone', 'purchase_date', 'order_number', 'product_name', 'product_article', 'product_price', 'return_reason']
        }
    ]

    for template_data in templates_data:
        obj, created = DocumentTemplate.objects.get_or_create(
            name=template_data['name'],
            defaults={
                'template_content': template_data['template_content']
            }
        )
        if created:
            obj.set_required_fields(template_data['required_fields'])
            obj.save()
            print(f"✓ Создан шаблон: {template_data['name']}")
        else:
            print(f"- Шаблон уже существует: {template_data['name']}")

    print("Загрузка тестовых данных завершена!")

if __name__ == '__main__':
    load_test_data()
