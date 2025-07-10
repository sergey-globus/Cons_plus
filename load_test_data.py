import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_portal.settings')
django.setup()

from apps.main.models import FAQ, DocumentTemplate

def load_test_data():
    print("Загрузка тестовых данных...")
    
    # Создание FAQ
    faq_data = [
        {
            'title': 'Как подать иск в суд?',
            'content': 'Для подачи иска в суд необходимо: 1) Составить исковое заявление; 2) Приложить необходимые документы; 3) Оплатить государственную пошлину; 4) Подать документы в суд.',
            'category': 'Судебные процедуры'
        },
        {
            'title': 'Какие документы нужны для развода?',
            'content': 'Для расторжения брака необходимы: свидетельство о заключении брака, паспорта супругов, свидетельства о рождении детей (при наличии), документы о совместном имуществе.',
            'category': 'Семейное право'
        },
        {
            'title': 'Как оформить наследство?',
            'content': 'Для оформления наследства обратитесь к нотариусу в течение 6 месяцев со дня смерти наследодателя. Принесите документы, подтверждающие родство и право на наследство.',
            'category': 'Наследственное право'
        },
        {
            'title': 'Что делать при увольнении?',
            'content': 'При увольнении работодатель обязан выдать трудовую книжку, справку о заработке, произвести окончательный расчет. Проверьте правильность оформления увольнения.',
            'category': 'Трудовое право'
        }
    ]

    for faq in faq_data:
        obj, created = FAQ.objects.get_or_create(
            title=faq['title'],
            defaults=faq
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
