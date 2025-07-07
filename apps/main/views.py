from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FAQ, Consultation, DocumentTemplate
from .forms import ConsultationForm, DocumentGeneratorForm
import requests
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from .models import LegalNews
from .forms import LegalNewsForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

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

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_legal_news(request):
    news_list = LegalNews.objects.all().order_by('-published_at')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    return render(request, 'admin/legal_news_list.html', {
        'news': news,
        'is_paginated': paginator.num_pages > 1
    })

def legal_news(request):
    news_list = LegalNews.objects.filter(is_published=True).order_by('-published_at')
    paginator = Paginator(news_list, 5)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    return render(request, 'main/legal_news.html', {
        'news': news,
        'is_paginated': paginator.num_pages > 1
    })

def news_detail(request, pk):
    article = get_object_or_404(LegalNews, pk=pk, is_published=True)
    return render(request, 'main/news_detail.html', {'article': article})

@user_passes_test(is_admin)
@require_http_methods(["POST"])
def toggle_news_status(request, news_id):
    news = get_object_or_404(LegalNews, id=news_id)
    try:
        data = json.loads(request.body)
        news.is_published = data.get('is_published', False)
        news.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            if request.user.is_authenticated:
                raise PermissionDenied
            else:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
        return view_func(request, *args, **kwargs)
    return wrapper

@staff_required
def admin_add_news(request):
    if request.method == 'POST':
        form = LegalNewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('admin_legal_news')
    else:
        form = LegalNewsForm()
    
    return render(request, 'admin/add_legal_news.html', {'form': form})

def add_news_redirect(request):
    if request.user.is_staff:
        return redirect('admin_add_news')
    else:
        messages.warning(request, 'Только администраторы могут добавлять новости')
        return redirect('legal_news')