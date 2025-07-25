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

import mammoth
from docxtpl import DocxTemplate
import tempfile
import os


def document_result(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)
    form_data = request.session.get('form_data', {})

    document_html = "<p>Файл шаблона не загружен.</p>"

    if template.word_document:
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp_path = tmp.name
                doc = DocxTemplate(template.word_document.path)
                doc.render(form_data if form_data else {})
                doc.save(tmp_path)

            with open(tmp_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                document_html = result.value
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    return render(request, "main/document_result.html", {
        "template_name": template.name,
        "document_html": document_html,
        "template_id": template.id,  # <-- добавьте это
    })


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
            
            Благодарим вас за обращение на наш сайт - МаркетНадзор!
            Ваш вопрос: "{consultation.question[:50]}..."
            
            Наши юристы рассмотрят вашу заявку в ближайшее время и свяжутся с вами в течение 24 часов, в том числе в выходные и праздничные дни.
            
            С уважением,
            Команда МаркетНадзор
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
                # Добавляем флаг для показа гифки
                request.session['show_success_gif'] = True

            except Exception as e:
                messages.error(request, f'Произошла ошибка при отправке email: {str(e)}')
                
            
            return redirect('consultation')
    else:
        form = ConsultationForm()
    return render(request, 'main/consultation.html', {'form': form})

import mammoth
import os
from django.shortcuts import render, get_object_or_404
from .models import DocumentTemplate


def preview_template(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)
    document_html = ""

    if template.word_template:
        with open(template.word_template.path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            document_html = result.value

    context = {
        'template': template,
        'document_html': document_html,
        'translated_fields': template.get_translated_fields(),
    }
    return render(request, "main/preview_template.html", context)

from django.urls import reverse


def document_generator(request):
    templates = DocumentTemplate.objects.all()

    selected_template_id = request.GET.get('template_id')
    try:
        selected_template_id_int = int(selected_template_id)
    except (TypeError, ValueError):
        selected_template_id_int = None

    if request.method == 'POST':
        print("DEBUG: request.POST:", request.POST)

        template_id = request.POST.get('template_id')
        if template_id:
            try:
                template = DocumentTemplate.objects.get(id=template_id)

                # Берём первое непустое значение из списка значений каждого ключа
                form_data = {}
                for k, v_list in request.POST.lists():
                    if k in ('csrfmiddlewaretoken', 'template_id'):
                        continue
                    value = next((v for v in v_list if v.strip()), '')
                    form_data[k] = value if value else f'[{k}]'

                request.session['form_data'] = form_data

                print("Parsed form_data:", form_data)

                return redirect(reverse('document_result', kwargs={'template_id': template.id}))

            except DocumentTemplate.DoesNotExist:
                messages.error(request, 'Выбранный шаблон не найден')

    return render(request, 'main/document_generator.html', {
        'templates': templates,
        'selected_template_id': selected_template_id_int,
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
    p.drawString(50, height - 50,
                 template_name.encode('utf-8').decode('utf-8') if font_name == 'Helvetica' else template_name)

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
                            p.drawString(50, y_position, current_line.encode('utf-8').decode(
                                'utf-8') if font_name == 'Helvetica' else current_line)
                        except:
                            p.drawString(50, y_position, current_line)
                        y_position -= 15
                    current_line = word + ' '
            if current_line:
                try:
                    p.drawString(50, y_position, current_line.encode('utf-8').decode(
                        'utf-8') if font_name == 'Helvetica' else current_line)
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


from django.http import HttpResponse
import tempfile
import os
from docxtpl import DocxTemplate

def download_word(request, template_id):
    # Получаем шаблон по id
    template = get_object_or_404(DocumentTemplate, id=template_id)

    # Получаем данные для подстановки
    form_data = request.session.get('form_data', {})

    if not template.word_document:
        messages.error(request, 'Шаблон документа не найден.')
        return redirect('document_generator')

    # Создаем временный файл
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            tmp_path = tmp.name
            doc = DocxTemplate(template.word_document.path)
            doc.render(form_data)
            doc.save(tmp_path)

        with open(tmp_path, 'rb') as f:
            response = HttpResponse(
                f.read(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{template.name}.docx"'
            return response
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

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

def privacy_policy(request):
    return render(request, 'main/privacy_policy.html')

def platform_economy_news_detail(request):
    """Детальная страница новости о платформенной экономике"""
    return render(request, 'main/platform_economy_news_detail.html')

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

def pretnezya(request):
    """Категория 'Неверная цена'"""
    return render(request, 'main/pretnezya.html')

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

    if not template.word_template:
        # Если файл шаблона не существует, возвращаем ошибку
        messages.error(request, "Файл шаблона Word не найден.")
        return redirect('preview_template', template_id=template.id)

    # Загружаем существующий .docx-файл шаблона
    doc = Document(template.word_template.path)

    # Проходим по всем параграфам документа
    for paragraph in doc.paragraphs:
        for field in template.required_fields:
            # Ищем и заменяем каждое поле вида {FIELD} на несколько пробелов (или табы)
            placeholder = f'{{{field}}}'
            if placeholder in paragraph.text:
                inline = paragraph.runs
                for i in range(len(inline)):
                    if placeholder in inline[i].text:
                        inline[i].text = inline[i].text.replace(placeholder, '        ')  # 8 пробелов или можно '\t'

    # Также можно обработать таблицы, если поля есть там
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for field in template.required_fields:
                        placeholder = f'{{{field}}}'
                        if placeholder in paragraph.text:
                            inline = paragraph.runs
                            for i in range(len(inline)):
                                if placeholder in inline[i].text:
                                    inline[i].text = inline[i].text.replace(placeholder, '        ')

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    filename = f'Пустой_{template.name}.docx'

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
import os

def download_empty_template_pdf(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)

    # Проверяем что PDF-шаблон доступен
    if not template.pdf_template:
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, "PDF шаблон не найден.")
        return redirect('preview_template', template_id=template.id)

    pdf_path = template.pdf_template.path

    if not os.path.exists(pdf_path):
        raise Http404("Файл PDF не найден")

    # Отдаем файл как скачиваемый
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Пустой_{template.name}.pdf"'
    return response