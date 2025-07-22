import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_portal.settings')
django.setup()

from apps.main.models import FAQ, DocumentTemplate

FAQ.objects.all().delete()
print("✓ Старые записи FAQ удалены")


def load_test_data():
    print("Загрузка тестовых данных...")

    # Создание FAQ
    faq_data = [
    {
        'title': 'Отмена заказа продавцом',
        'synonyms': 'отказ продавцом, отмена покупки продавцом, права покупателя',
        'description': 'Что делать, если продавец или маркетплейс отменил ваш заказ в одностороннем порядке',
        'tags': 'Отмена заказа,Права покупателя,Продавец',
        'icon_class': 'fas fa-times-circle',
        'url_name': 'order-cancellation',
    },
    {
        'title': 'Ошибочная цена товара',
        'synonyms': 'техническая ошибка в цене',
        'description': 'Может ли продавец отказаться от исполнения договора из-за технической ошибки в цене',
        'tags': 'Ошибка цены,Публичная оферта,Товар',
        'icon_class': 'fas fa-exclamation-triangle',
        'url_name': 'price-error',
    },
    {
        'title': 'Что делать, если информация о товаре не соответствует действительности?',
        'synonyms': 'недостоверная информация, неправильное описание, обман покупателя',
        'description': 'Что делать, если полученный товар не соответствует описанию на маркетплейсе',
        'tags': 'Обман покупателя,Возврат денег, Товар',
        'icon_class': 'fas fa-info-circle',
        'url_name': 'art10',
    },
    {
        'title': 'Что делать, если пришел товар ненадлежащего качества?',
        'synonyms': 'бракованный товар, дефекты, недостатки товара',
        'description': 'Права потребителя при получении товара с дефектами или недостатками',
        'tags': 'Товар, Брак',
        'icon_class': 'fas fa-tags',
        'url_name': 'art1',
    },
    {
        'title': 'Можно ли вернуть товар после вскрытия упаковки?',
        'synonyms': 'нарушенная упаковка, вскрытая коробка, сохранение товарного вида',
        'description': 'Можно ли вернуть товар, если упаковка была вскрыта или повреждена',
        'tags': 'Упаковка,Товар,Возврат',
        'icon_class': 'fas fa-box-open',
        'url_name': 'art9',
    },
    {
        'title': 'Вправе ли продавец удерживать плату за возврат товара?',
        'synonyms': 'стоимость возврата, расходы на доставку, удержание средств',
        'description': 'В каких случаях продавец может удерживать плату за возврат товара',
        'tags': 'Расходы,Доставка,Возврат средств, Продавец',
        'icon_class': 'fas fa-money-bill-wave',
        'url_name': 'art8',
    },
    {
        'title': 'Является ли обязательным претензионный (досудебный) порядок в спорах по защите прав потребителей?',
        'synonyms': 'претензионный порядок, обязательная претензия, досудебное урегулирование',
        'description': 'Когда нужно направлять претензию перед обращением в суд',
        'tags': 'Претензия,Досудебное урегулирование,Суд',
        'icon_class': 'fas fa-gavel',
        'url_name': 'art2',
    },
    {
        'title': 'Как составить исковое заявление?',
        'synonyms': 'иск в суд, образец иска, как подать в суд',
        'description': 'Пошаговая инструкция по подготовке иска в суд по защите прав потребителей',
        'tags': 'Исковое заявление,Суд,Образец',
        'icon_class': 'fas fa-file-alt',
        'url_name': 'art3',
    },
    {
        'title': 'Как вернуть товар ненадлежащего качества?',
        'synonyms': 'технически сложные товары, нижнее белье, парфюмерия',
        'description': 'Можно ли вернуть товары ненадлежащего качества',
        'tags': 'Невозвратные товары, Качество',
        'icon_class': 'fas fa-ban',
        'url_name': 'art4',
    },
    {
        'title': 'Как вернуть товар надлежащего качества?',
        'synonyms': 'технически сложные товары, нижнее белье, парфюмерия',
        'description': 'Можно ли вернуть товары, которые подлежат возврату и обмену',
        'tags': 'Качество',
        'icon_class': 'fas fa-ban',
        'url_name': 'art5',
    },
    {
        'title': 'Как составить претензию к продавцу на маркетплейсе',
        'synonyms': 'технически сложные товары, нижнее белье, парфюмерия',
        'description': 'Составление претензии продавцу',
        'tags': 'Суд, образец, претензия',
        'icon_class': 'fas fa-ban',
        'url_name': 'pretnezya',
    },
    {
        'title': 'Можно ли вернуть товар, входящий в перечень невозвратных товаров?',
        'synonyms': 'технически сложные товары, нижнее белье, парфюмерия',
        'description': 'Можно ли вернуть товары, которые обычно не подлежат возврату и обмену',
        'tags': 'Невозвратные товары, Доставка, Товар',
        'icon_class': 'fas fa-ban',
        'url_name': 'art7',
    }
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
    # DocumentTemplate.objects.all().delete()
    # print("✓ Старые шаблоны удалены")

    from django.db import connection
    from apps.main.models import DocumentTemplate

    # Сброс автоинкремента (id) для таблицы DocumentTemplate
    DocumentTemplate.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name=%s;", [DocumentTemplate._meta.db_table])
    print("ID автоинкремент сброшен до 1")

    # Создание новых шаблонов документов, связанных с маркетплейсами
    templates_data = [
        {
            'name': 'Шаблон искового заявления (общий)',
            'word_document_path': 'documents\\src\\docx\\Шаблон искового заявления (общий).docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон искового заявления (общий).docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон искового заявления (общий).pdf',
            'template_content': "",
            'required_fields': [],
        },
        {
            'name': 'Претензия (товар ненадлежащего качества)',
            'word_document_path': 'documents\\src\\docx\\Претензия_1_товар_ненадлежащего_качества.docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон_Претензия_1_товар_ненадлежащего_качества.docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон_Претензия_1_товар_ненадлежащего_качества.pdf',
            'template_content': "",
            'required_fields': [
                'SELLER_NAME', 'SELLER_ADDRESS', 'BUYER_NAME', 'BUYER_ADDRESS', 'BUYER_PHONE',
                'BUYER_EMAIL', 'PURCHASE_DAY', 'PURCHASE_MONTH', 'PURCHASE_YEAR',
                'MARKETPLACE', 'PRODUCT_NAME', 'PRODUCT_PRICE', 'PAYMENT_PROOF',
                'DELIVERY_DAY', 'DELIVERY_MONTH', 'DELIVERY_YEAR', 'DEFECT_DETECTION_PERIOD',
                'DEFECT_DESCRIPTION', 'WARRANTY_PERIOD', 'CLAIM_REQUIREMENTS',
                'CURRENT_DAY', 'CURRENT_MONTH', 'CURRENT_YEAR',
            ]
        },
        {
            'name': 'Претензия (односторонняя отмена заказа)',
            'word_document_path': 'documents\\src\\docx\\Претензия_2_односторонняя_отмена_заказа.docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон_Претензия_2_односторонняя_отмена_заказа.docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон_Претензия_2_односторонняя_отмена_заказа.pdf',
            'template_content': "",
            'required_fields': [
                'SELLER_NAME', 'SELLER_ADDRESS', 'BUYER_NAME', 'BUYER_ADDRESS', 'BUYER_PHONE',
                'BUYER_EMAIL', 'PURCHASE_DAY', 'PURCHASE_MONTH', 'PURCHASE_YEAR',
                'MARKETPLACE', 'PRODUCT_NAME', 'PRODUCT_PRICE', 'PAYMENT_PROOF',
                'CANCEL_DAY', 'CANCEL_MONTH', 'CANCEL_YEAR', 'ADDITIONAL_CIRCUMSTANCES',
                'CLAIM_REQUIREMENTS',
                'CURRENT_DAY', 'CURRENT_MONTH', 'CURRENT_YEAR',
            ],
        },
        {
            'name': 'Претензия (недостоверная информация)',
            'word_document_path': 'documents\\src\\docx\\Претензия_3_недостоверная_информация.docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон_Претензия_3_недостоверная_информация.docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон_Претензия_3_недостоверная_информация.pdf',
            'template_content': "",
            'required_fields': [
                'SELLER_NAME', 'SELLER_ADDRESS', 'BUYER_NAME', 'BUYER_ADDRESS', 'BUYER_PHONE',
                'BUYER_EMAIL', 'PRODUCT_NAME', 'CIRCUMSTANCES',
                'CLAIM_REQUIREMENTS',
                'CURRENT_DAY', 'CURRENT_MONTH', 'CURRENT_YEAR',
            ],
        },
        {
            'name': 'Иск (возврат товара надлежащего качества)',
            'word_document_path': 'documents\\src\\docx\\Возврат_товара_надлежащего_качества.docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон_Возврат_товара_надлежащего_качества.docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон_Возврат_товара_надлежащего_качества.pdf',
            'template_content': "",
            'required_fields': [
                'COURT_NAME',
                'PLAINTIFF_NAME',
                'PLAINTIFF_BIRTH_DATE',
                'PLAINTIFF_BIRTH_PLACE',
                'PLAINTIFF_ADDRESS',
                'PLAINTIFF_PASSPORT_INFO',
                'DEFENDANT_NAME',
                'DEFENDANT_BIRTH_DATE',
                'DEFENDANT_BIRTH_PLACE',
                'DEFENDANT_ADDRESS',
                'DEFENDANT_PASSPORT_INFO',
                'CLAIM_AMOUNT',
                'SITUATION_DESCRIPTION',
                'CLAIM_DEMANDS',
                'DATE_DAY',
                'DATE_MONTH',
                'DATE_YEAR',
            ],
        },
        {
            'name': 'Иск (возврат товара ненадлежащего качества)',
            'word_document_path': 'documents\\src\\docx\\Возврат_товара_ненадлежащего_качества.docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон_Возврат_товара_ненадлежащего_качества.docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон_Возврат_товара_ненадлежащего_качества.pdf',
            'template_content': "",
            'required_fields': [
                'COURT_NAME',
                'PLAINTIFF_NAME',
                'PLAINTIFF_BIRTH_DATE',
                'PLAINTIFF_BIRTH_PLACE',
                'PLAINTIFF_ADDRESS',
                'PLAINTIFF_PASSPORT_INFO',
                'DEFENDANT_NAME',
                'DEFENDANT_BIRTH_DATE',
                'DEFENDANT_BIRTH_PLACE',
                'DEFENDANT_ADDRESS',
                'DEFENDANT_PASSPORT_INFO',
                'CLAIM_AMOUNT',
                'SITUATION_DESCRIPTION',
                'CLAIM_DEMANDS',
                'DATE_DAY',
                'DATE_MONTH',
                'DATE_YEAR',
            ],
        },
        {
            'name': 'Иск (недостоверная информация о товаре)',
            'word_document_path': 'documents\\src\\docx\\Недостоверная_информация_о_товаре.docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон_Недостоверная_информация_о_товаре.docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон_Недостоверная_информация_о_товаре.pdf',
            'template_content': "",
            'required_fields': [
                'COURT_NAME',
                'PLAINTIFF_NAME',
                'PLAINTIFF_BIRTH_DATE',
                'PLAINTIFF_BIRTH_PLACE',
                'PLAINTIFF_ADDRESS',
                'PLAINTIFF_PASSPORT_INFO',
                'DEFENDANT_NAME',
                'DEFENDANT_BIRTH_DATE',  # Обратите внимание, что здесь переменная DEFENDANT_BIRTH_DATE
                'DEFENDANT_BIRTH_PLACE',  # и DEFENDANT_BIRTH_PLACE были не совсем корректны в вашем тексте
                'DEFENDANT_ADDRESS',
                'DEFENDANT_PASSPORT_INFO',
                'CLAIM_AMOUNT',
                'SITUATION_DESCRIPTION',
                'CLAIM_DEMANDS',
                'DATE_DAY',
                'DATE_MONTH',
                'DATE_YEAR',
            ],
        },
        {
            'name': 'Иск (отмена заказа продавцом)',
            'word_document_path': 'documents\\src\\docx\\Отмена_заказа_продавцом.docx',
            'word_template_path': 'documents\\src\\docx\\Шаблон_Отмена_заказа_продавцом.docx',
            'pdf_template_path': 'documents\\src\\pdf\\Шаблон_Отмена_заказа_продавцом.pdf',
            'template_content': "",  # Можно заполнить при необходимости
            'required_fields': [
                'COURT_NAME',
                'PLAINTIFF_NAME',
                'PLAINTIFF_BIRTH_DATE',
                'PLAINTIFF_BIRTH_PLACE',
                'PLAINTIFF_ADDRESS',
                'PLAINTIFF_PASSPORT_INFO',
                'DEFENDANT_NAME',
                'DEFENDANT_BIRTH_DATE',
                'DEFENDANT_BIRTH_PLACE',
                'DEFENDANT_ADDRESS',
                'DEFENDANT_PASSPORT_INFO',
                'CLAIM_AMOUNT',
                'ORDER_CANCEL_DATE_DAY',
                'ORDER_CANCEL_DATE_MONTH',
                'ORDER_CANCEL_DATE_YEAR',
                'ADDITIONAL_CIRCUMSTANCES',
                'SITUATION_DESCRIPTION',
                'CLAIM_DEMANDS',
                'DATE_DAY',
                'DATE_MONTH',
                'DATE_YEAR',
            ],
        }
    ]

    from django.conf import settings
    from django.core.files import File

    for template_data in templates_data:
        obj, created = DocumentTemplate.objects.get_or_create(
            name=template_data['name'],
            defaults={
                'template_content': template_data['template_content']
            }
        )

        # Функция для сохранения файла в FileField с заменой существующего
        def save_file(obj, field_name, file_path):
            from django.conf import settings
            from django.core.files import File
            import os

            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(full_path):
                # 1. Удалить старый файл и обнулить поле
                filefield = getattr(obj, field_name)
                if filefield and filefield.name:
                    filefield.delete(save=False)
                    setattr(obj, field_name, None)

                # 2. Сохранить новый файл
                with open(full_path, 'rb') as f:
                    django_file = File(f)
                    filefield.save(os.path.basename(file_path), django_file, save=False)
            else:
                print(f"Файл не найден: {full_path}")

        # Если объект уже существует — обновляем файлы и поля
        update_needed = False
        if not created:
            # Обновим файлы, если указаны
            save_file(obj, 'word_document', template_data['word_document_path'])
            save_file(obj, 'word_template', template_data['word_template_path'])
            save_file(obj, 'pdf_template', template_data['pdf_template_path'])
            obj.save()

            # Обновим required_fields и template_content, если нужно
            obj.set_required_fields(template_data['required_fields'])
            obj.template_content = template_data['template_content']
            update_needed = True
        else:
            # Для нового объекта тоже сохраняем файлы
            save_file(obj, 'word_document', template_data['word_document_path'])
            save_file(obj, 'word_template', template_data['word_template_path'])
            save_file(obj, 'pdf_template', template_data['pdf_template_path'])
            obj.save()

            obj.set_required_fields(template_data['required_fields'])
            update_needed = True

        if update_needed:
            obj.save()

        print(f"{'✓ Создан' if created else '↺ Обновлен'} шаблон: {obj.name}")

    print("Загрузка тестовых данных завершена!")

if __name__ == '__main__':
    load_test_data()
