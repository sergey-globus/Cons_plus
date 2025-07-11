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
            
            Наши юристы рассмотрят вашу заявку в ближайшее время и свяжутся с вами по email.
            
            С уважением,
            Команда Правового портала
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],  # Используем расшифрованный email
                    fail_silently=False,
                )
                messages.success(request, 'Ваша заявка принята! На ваш email отправлено подтверждение.')
            except Exception as e:
                messages.error(request, f'Произошла ошибка при отправке email: {str(e)}')
                # Можно также залогировать ошибку
            
            return redirect('consultation')
    else:
        form = ConsultationForm()
    return render(request, 'main/consultation.html', {'form': form})

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
    """Страница правовых новостей с фильтрацией"""
    category = request.GET.get('category', 'all')
    
    all_news = [
        {
            'title': 'Изменения в Гражданском кодексе РФ',
            'content': 'Вступили в силу новые изменения в ГК РФ, касающиеся защиты прав потребителей при дистанционных покупках.',
            'published_at': '08.07.2025',
            'source': 'Официальный портал правовой информации',
            'url': 'http://pravo.gov.ru',
            'category': 'consumer'
        },
        {
            'title': 'Новые правила возврата товаров на маркетплейсах',
            'content': 'Роспотребнадзор разъяснил порядок возврата товаров, приобретенных через интернет-площадки.',
            'published_at': '07.07.2025',
            'source': 'Роспотребнадзор',
            'url': 'https://rospotrebnadzor.ru',
            'category': 'consumer'
        },
        {
            'title': 'Изменения в трудовом законодательстве',
            'content': 'Приняты поправки в Трудовой кодекс РФ, касающиеся дистанционной работы и электронного документооборота.',
            'published_at': '06.07.2025',
            'source': 'Минтруд России',
            'url': 'https://mintrud.gov.ru',
            'category': 'labor'
        },
        {
            'title': 'Новые требования к договорам аренды',
            'content': 'Вступили в силу изменения в жилищном законодательстве, упрощающие процедуру заключения договоров аренды.',
            'published_at': '05.07.2025',
            'source': 'Минстрой России',
            'url': 'https://minstroyrf.gov.ru',
            'category': 'housing'
        },
        {
            'title': 'Обновления в налоговом законодательстве',
            'content': 'Федеральная налоговая служба опубликовала разъяснения по применению новых налоговых льгот для малого и среднего бизнеса.',
            'published_at': '04.07.2025',
            'source': 'ФНС России',
            'url': 'https://nalog.gov.ru',
            'category': 'tax'
        }
    ]
    
    if category != 'all':
        filtered_news = [news for news in all_news if news['category'] == category]
    else:
        filtered_news = all_news
    
    news = {'articles': filtered_news}
    
    return render(request, 'main/legal_news.html', {
        'news': news,
        'current_category': category
    })

def reference_materials(request):
    """Главная страница справочных материалов"""
    return render(request, 'main/reference_materials.html')

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
