from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import FAQ, Consultation, DocumentTemplate
from .forms import ConsultationForm, DocumentGeneratorForm
import requests
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from docx import Document
from docx.shared import Inches
from django.db.models import Q
from django.shortcuts import get_object_or_404
from docx.shared import Pt, Cm  


def index(request):
    return render(request, 'main/index.html')

from django.core.mail import send_mail
from django.conf import settings

def consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            # Сохраняем форму, данные автоматически зашифруются через свойства модели
            consultation = form.save()
            
            # Получаем расшифрованные данные через свойства
            first_name = consultation.first_name
            last_name = consultation.last_name
            email = consultation.email
            
            subject = 'Ваша заявка на консультацию принята'
            message = f'''
            Уважаемый(ая) {first_name} {last_name},

            Благодарим вас за обращение на наш правовой портал!
            Ваш вопрос: "{consultation.question[:50]}..."
            
            Наши юристы рассмотрят вашу заявку в ближайшее время и свяжутся с вами в течение 3 дней.
            
            С уважением,
            Команда Правового портала
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email], 
                    fail_silently=False,
                )
                messages.success(request, 'Ваша заявка принята! На ваш email отправлено подтверждение.')
            except Exception as e:
                messages.error(request, f'Произошла ошибка при отправке email: {str(e)}')
                
            
            return redirect('consultation')
    else:
        form = ConsultationForm()
    return render(request, 'main/consultation.html', {'form': form})

def preview_template(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)
    
    context = {
        'template': template,
        'translated_fields': template.get_translated_fields()
    }
    
    return render(request, 'main/preview_template.html', context)

def document_generator(request):
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        if template_id:
            try:
                template = DocumentTemplate.objects.get(id=template_id)
                
                # Собираем данные из формы
                form_data = {}
                for field in request.POST:
                    if field != 'csrfmiddlewaretoken' and field != 'template_id':
                        form_data[field] = request.POST.get(field, '')
                
                # Заменяем пустые поля на заглушки
                for field in form_data:
                    if not form_data[field]:
                        form_data[field] = f'[{field}]'
                
                # Генерируем документ
                try:
                    generated_document = template.template_content.format(**form_data)
                    
                    # Сохраняем данные в сессии для скачивания
                    request.session['generated_document'] = generated_document
                    request.session['template_name'] = template.name
                    request.session['form_data'] = form_data
                    
                    return render(request, 'main/document_result.html', {
                        'document': generated_document,
                        'template_name': template.name
                    })
                except KeyError as e:
                    messages.error(request, f'Ошибка в шаблоне: {e}')
                
            except DocumentTemplate.DoesNotExist:
                messages.error(request, 'Выбранный шаблон не найден')
    
    templates = DocumentTemplate.objects.all()
    return render(request, 'main/document_generator.html', {
        'templates': templates
    })

def download_pdf(request):
    """Скачивание документа в формате PDF"""
    document_text = request.session.get('generated_document', '')
    template_name = request.session.get('template_name', 'Документ')
    
    if not document_text:
        messages.error(request, 'Документ не найден. Создайте документ заново.')
        return redirect('document_generator')
    
    # Создаем PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Настройки шрифта
    try:
        # Пытаемся использовать системный шрифт с поддержкой кириллицы
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf')
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            font_name = 'DejaVuSans'
        else:
            font_name = 'Helvetica'
    except:
        font_name = 'Helvetica'
    
    # Заголовок
    p.setFont(font_name, 16)
    p.drawString(50, height - 50, template_name.encode('utf-8').decode('utf-8') if font_name == 'Helvetica' else template_name)
    
    # Содержимое документа
    p.setFont(font_name, 12)
    lines = document_text.split('\n')
    y_position = height - 100
    
    for line in lines:
        if y_position < 50:  # Новая страница
            p.showPage()
            p.setFont(font_name, 12)
            y_position = height - 50
        
        # Обрабатываем длинные строки
        if len(line) > 80:
            words = line.split(' ')
            current_line = ''
            for word in words:
                if len(current_line + word) < 80:
                    current_line += word + ' '
                else:
                    if current_line:
                        try:
                            p.drawString(50, y_position, current_line.encode('utf-8').decode('utf-8') if font_name == 'Helvetica' else current_line)
                        except:
                            p.drawString(50, y_position, current_line)
                        y_position -= 15
                    current_line = word + ' '
            if current_line:
                try:
                    p.drawString(50, y_position, current_line.encode('utf-8').decode('utf-8') if font_name == 'Helvetica' else current_line)
                except:
                    p.drawString(50, y_position, current_line)
                y_position -= 15
        else:
            try:
                p.drawString(50, y_position, line.encode('utf-8').decode('utf-8') if font_name == 'Helvetica' else line)
            except:
                p.drawString(50, y_position, line)
            y_position -= 15
    
    p.save()
    buffer.seek(0)
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{template_name}.pdf"'
    return response

def download_word(request):
    """Скачивание документа в формате Word"""
    document_text = request.session.get('generated_document', '')
    template_name = request.session.get('template_name', 'Документ')
    
    if not document_text:
        messages.error(request, 'Документ не найден. Создайте документ заново.')
        return redirect('document_generator')
    
    # Создаем Word документ
    doc = Document()
    
    # Добавляем заголовок
    title = doc.add_heading(template_name, 0)
    title.alignment = 1  # Центрирование
    
    # Добавляем содержимое
    paragraphs = document_text.split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            p = doc.add_paragraph(paragraph.strip())
    
    # Сохраняем в буфер
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{template_name}.docx"'
    return response

def legal_news(request):
    """Страница правовых новостей (только новость о платформенной экономике)"""
    all_news = [
        {
            'title': 'Государственная Дума приняла законопроект о платформенной экономике в первом чтении',
            'content': 'Как новый законопроект защитит права продавцов и покупателей на маркетплейсах...',
            'published_at': '21.07.2025',
            'source': 'Государственная Дума РФ',
            'url': '/news/platform-economy/',  # Внутренняя ссылка на полную новость
        }
    ]
    
    return render(request, 'main/legal_news.html')

def platform_economy_news_detail(request):
    """Детальная страница новости о платформенной экономике"""
    return render(request, 'main/platform_economy_news_detail.html')

def privacy_policy(request):
    return render(request, 'main/privacy_policy.html')

def reference_materials(request):
    query = request.GET.get('q', '').strip()

    if query:
        articles = FAQ.objects.filter(
            Q(title__iregex=query) | Q(description__iregex=query) | Q(synonyms__iregex=query),
            is_active=True
        )
    else:
        articles = FAQ.objects.filter(is_active=True)

    for article in articles:
        article.tags_list = [tag.strip() for tag in article.tags.split(',')] if article.tags else []

    # Отладочная печать - что мы передаем в шаблон
    print(f"Total articles found: {articles.count()}")
    for a in articles:
        print(f"Article: {a.title}, tags: {a.tags_list}")

    context = {
        'articles': articles,
        'query': query,
    }

    return render(request, 'main/reference_materials.html', context)


def marketplace_rights(request):
    """Обновленная статья о правах пользователей на маркетплейсах"""
    return render(request, 'main/marketplace_rights.html')

def order_cancellation(request):
    """Новая статья об отмене заказа продавцом"""
    return render(request, 'main/order_cancellation.html')

def price_error(request):
    """Новая статья об ошибочной цене"""
    return render(request, 'main/price_error.html')

def glossary(request):
    """Глоссарий правовых терминов"""
    return render(request, 'main/glossary.html')

def price_category(request):
    """Категория 'Неверная цена'"""
    return render(request, 'main/price.html')

def return_category(request):
    """Категория 'Возврат товара'"""
    articles = FAQ.objects.filter(tags__icontains='Товар') | \
               FAQ.objects.filter(tags__icontains='Качество') | \
               FAQ.objects.filter(tags__icontains='Брак') | \
               FAQ.objects.filter(tags__icontains='Упаковка')
    
    # Добавляем tags_list к каждому объекту
    for article in articles:
        article.tags_list = [tag.strip() for tag in article.tags.split(',')]
    
    context = {
        'articles': articles,
        'page_title': 'Проблемы с товаром',
        'page_description': 'Решение проблем, связанных с качеством и характеристиками товаров'
    }
    return render(request, 'main/return.html', context)

def seller_category(request):
    """Категория 'Проблема с продавцом'"""
    articles = FAQ.objects.filter(tags__icontains='Продавец') | \
               FAQ.objects.filter(tags__icontains='Отмена') | \
               FAQ.objects.filter(tags__icontains='Оферта')
    
    for article in articles:
        article.tags_list = [tag.strip() for tag in article.tags.split(',')]
    
    context = {
        'articles': articles,
        'page_title': 'Проблемы с продавцом',
        'page_description': 'Решение конфликтов и споров с продавцами на маркетплейсах'
    }
    return render(request, 'main/seller.html', context)

def delivery_category(request):
    """Категория 'Не привезли товар'"""
    articles = FAQ.objects.filter(tags__icontains='Доставка') | \
               FAQ.objects.filter(tags__icontains='Получение')
    
    for article in articles:
        article.tags_list = [tag.strip() for tag in article.tags.split(',')]
    
    context = {
        'articles': articles,
        'page_title': 'Проблемы с доставкой',
        'page_description': 'Решение вопросов, связанных с доставкой товаров'
    }
    return render(request, 'main/delivery.html', context)

def damaged_category(request):
    """Категория 'Поврежденный товар'"""
    return render(request, 'main/damaged.html')

def delivery_terms_category(request):
    """Категория 'Условия доставки'"""
    return render(request, 'main/delivery_terms.html')

def bad_goods_delivered(request):
    return render(request, 'main/bad_goods_delivered.html')

def dosydebnii_isk(request):
    return render(request, 'main/dosydebnii_isk.html')

def isk_zyavlenie(request):
    return render(request, 'main/isk_zyavlenie.html')

def return_bad(request):
    return render(request, 'main/return_bad.html')

def return_good(request):
    return render(request, 'main/return_good.html')

def return_nevozvrat(request):
    return render(request, 'main/return_nevozvrat.html')

def return_plata(request):
    return render(request, 'main/return_plata.html')

def return_vskr_ypakovka(request):
    return render(request, 'main/return_vskr_ypakovka.html')

def wrong_price(request):
    return render(request, 'main/wrong_price.html')

def download_empty_template(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)
    
    doc = Document()

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    content = template.template_content

    for field in template.required_fields:
        content = content.replace(f'{{{field}}}', '        ') 
    
    for paragraph in content.split('\n'):
        if paragraph.strip():
            p = doc.add_paragraph()
            runs = paragraph.split('        ')  
            
            for i, run_text in enumerate(runs):
                if run_text:
                    p.add_run(run_text)

                if i < len(runs) - 1:
                    p.add_run().add_tab()

    for paragraph in doc.paragraphs:
        paragraph.paragraph_format.tab_stops.add_tab_stop(Cm(4))  
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="Пустой_{template.name}.docx"'
    return response