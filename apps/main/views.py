from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FAQ, Consultation, DocumentTemplate
from .forms import ConsultationForm, DocumentGeneratorForm
import requests
from django.conf import settings

def index(request):
    faqs = FAQ.objects.filter(is_active=True)[:6]
    return render(request, 'main/index.html', {'faqs': faqs})

def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True)
    categories = FAQ.objects.values_list('category', flat=True).distinct()
    return render(request, 'main/faq.html', {
        'faqs': faqs,
        'categories': categories
    })

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

@login_required
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
    # Интеграция с внешним API для получения правовых новостей
    news = []
    if settings.LEGAL_API_KEY:
        try:
            response = requests.get(
                'https://api.legal-news.com/v1/news',
                headers={'Authorization': f'Bearer {settings.LEGAL_API_KEY}'},
                timeout=10
            )
            if response.status_code == 200:
                news = response.json().get('articles', [])
        except requests.RequestException:
            pass
    
    return render(request, 'main/legal_news.html', {'news': news})
