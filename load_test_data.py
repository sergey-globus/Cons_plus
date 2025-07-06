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

    # Создание шаблонов документов
    templates_data = [
        {
            'name': 'Договор купли-продажи недвижимости',
            'template_content': '''ДОГОВОР КУПЛИ-ПРОДАЖИ НЕДВИЖИМОСТИ

г. Москва                                                    {date}

Продавец: {last_name} {first_name} {middle_name}, паспорт: {passport_number}
Покупатель: ________________________

Предмет договора: Продавец обязуется передать в собственность Покупателю недвижимое имущество.

Договор № {contract_number}

Подписи сторон:
Продавец: ________________
Покупатель: ________________''',
            'required_fields': ['first_name', 'last_name', 'middle_name', 'passport_number', 'contract_number', 'date']
        },
        {
            'name': 'Доверенность на представление интересов',
            'template_content': '''ДОВЕРЕННОСТЬ

г. Москва                                                    {date}

Я, {last_name} {first_name} {middle_name}, паспорт: {passport_number}, настоящей доверенностью уполномочиваю ________________________ представлять мои интересы в ________________________.

Доверенность выдана сроком на ________________________.

Подпись доверителя: ________________
                    {last_name} {first_name} {middle_name}''',
            'required_fields': ['first_name', 'last_name', 'middle_name', 'passport_number', 'date']
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
