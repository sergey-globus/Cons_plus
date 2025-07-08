from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FAQ, Consultation, DocumentTemplate
from .forms import ConsultationForm, DocumentGeneratorForm
import requests
from django.conf import settings

def index(request):
    return render(request, 'main/index.html')

def consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваша заявка принята! Мы свяжемся с вами в ближайшее время.')
            return redirect('consultation')
    else:
        form = ConsultationForm()
    return render(request, 'main/consultation.html', {'form': form})

def document_generator(request):
    if request.method == 'POST':
        form = DocumentGeneratorForm(request.POST)
        if form.is_valid():
            template = DocumentTemplate.objects.get(id=form.cleaned_data['template_id'])
            generated_document = template.template_content.format(**form.cleaned_data)
            return render(request, 'main/document_result.html', {
                'document': generated_document,
                'template_name': template.name
            })
    else:
        form = DocumentGeneratorForm()
    
    templates = DocumentTemplate.objects.all()
    return render(request, 'main/document_generator.html', {
        'form': form,
        'templates': templates
    })

def legal_news(request):
    """Страница правовых новостей с реальными ссылками"""
    # Создаем структуру данных, совместимую с шаблоном
    news = {
        'articles': [
            {
                'title': 'Изменения в Гражданском кодексе РФ',
                'content': 'Вступили в силу новые изменения в ГК РФ, касающиеся защиты прав потребителей при дистанционных покупках. Изменения направлены на усиление защиты прав покупателей при совершении покупок через интернет-площадки.',
                'published_at': '08.07.2025',
                'source': 'Официальный портал правовой информации',
                'url': 'http://pravo.gov.ru'
            },
            {
                'title': 'Новые правила возврата товаров на маркетплейсах',
                'content': 'Роспотребнадзор разъяснил порядок возврата товаров, приобретенных через интернет-площадки. Новые разъяснения касаются сроков возврата и требований к состоянию товара.',
                'published_at': '07.07.2025',
                'source': 'Роспотребнадзор',
                'url': 'https://rospotrebnadzor.ru'
            },
            {
                'title': 'Изменения в трудовом законодательстве',
                'content': 'Приняты поправки в Трудовой кодекс РФ, касающиеся дистанционной работы и электронного документооборота. Изменения упрощают процедуры оформления трудовых отношений.',
                'published_at': '06.07.2025',
                'source': 'Минтруд России',
                'url': 'https://mintrud.gov.ru'
            },
            {
                'title': 'Новые требования к договорам аренды',
                'content': 'Вступили в силу изменения в жилищном законодательстве, упрощающие процедуру заключения договоров аренды. Новые правила направлены на защиту прав как арендаторов, так и арендодателей.',
                'published_at': '05.07.2025',
                'source': 'Минстрой России',
                'url': 'https://minstroyrf.gov.ru'
            },
            {
                'title': 'Обновления в налоговом законодательстве',
                'content': 'Федеральная налоговая служба опубликовала разъяснения по применению новых налоговых льгот для малого и среднего бизнеса. Изменения вступят в силу с 1 августа 2025 года.',
                'published_at': '04.07.2025',
                'source': 'ФНС России',
                'url': 'https://nalog.gov.ru'
            }
        ]
    }
    
    return render(request, 'main/legal_news.html', {'news': news})

def reference_materials(request):
    """Главная страница справочных материалов с выбором статей"""
    return render(request, 'main/reference_materials.html')

def marketplace_rights(request):
    """Страница с информацией о правах пользователей на маркетплейсах"""
    return render(request, 'main/marketplace_rights.html')
