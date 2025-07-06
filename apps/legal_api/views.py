from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from apps.main.models import DocumentTemplate
from .services import LegalNewsService
import json

@require_http_methods(["GET"])
def get_legal_news(request):
    """API для получения правовых новостей"""
    service = LegalNewsService()
    limit = int(request.GET.get('limit', 10))
    news = service.get_news(limit)
    return JsonResponse(news)

@require_http_methods(["GET"])
def search_legal_info(request):
    """API для поиска правовой информации"""
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Параметр q обязателен'}, status=400)
    
    service = LegalNewsService()
    results = service.search_legal_info(query)
    return JsonResponse(results)

@require_http_methods(["GET"])
def get_template_fields(request, template_id):
    """API для получения полей шаблона документа"""
    template = get_object_or_404(DocumentTemplate, id=template_id)
    
    # Формируем список полей с их метаданными
    fields = []
    field_mapping = {
        'first_name': {'name': 'first_name', 'label': 'Имя', 'type': 'text'},
        'last_name': {'name': 'last_name', 'label': 'Фамилия', 'type': 'text'},
        'middle_name': {'name': 'middle_name', 'label': 'Отчество', 'type': 'text'},
        'passport_number': {'name': 'passport_number', 'label': 'Номер паспорта', 'type': 'text'},
        'contract_number': {'name': 'contract_number', 'label': 'Номер договора', 'type': 'text'},
        'date': {'name': 'date', 'label': 'Дата', 'type': 'date'},
    }
    
    for field_name in template.required_fields:
        if field_name in field_mapping:
            fields.append(field_mapping[field_name])
    
    return JsonResponse({
        'template_id': template_id,
        'template_name': template.name,
        'fields': fields
    })

@csrf_exempt
@require_http_methods(["POST"])
def preview_document(request):
    """API для предварительного просмотра документа"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        
        if not template_id:
            return JsonResponse({'error': 'template_id обязателен'}, status=400)
        
        template = get_object_or_404(DocumentTemplate, id=template_id)
        
        # Добавляем текущую дату если не указана
        if 'date' not in data:
            from datetime import datetime
            data['date'] = datetime.now().strftime('%d.%m.%Y')
        
        # Генерируем предварительный просмотр
        try:
            preview = template.template_content.format(**data)
            return JsonResponse({
                'success': True,
                'preview': preview,
                'template_name': template.name
            })
        except KeyError as e:
            return JsonResponse({
                'error': f'Отсутствует обязательное поле: {str(e)}'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный формат JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
