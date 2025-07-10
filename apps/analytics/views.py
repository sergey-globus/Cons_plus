from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import csv
from .models import PageVisit

@staff_member_required
def analytics_dashboard(request):
    # Статистика за последние 30 дней
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Общая статистика
    total_visits = PageVisit.objects.count()
    visits_last_30_days = PageVisit.objects.filter(visited_at__gte=thirty_days_ago).count()
    unique_visitors = PageVisit.objects.values('ip_address').distinct().count()
    
    # Популярные страницы
    popular_pages = PageVisit.objects.values('page_url').annotate(
        visit_count=Count('id')
    ).order_by('-visit_count')[:10]
    
    # Посещения по дням (последние 7 дней)
    daily_visits = []
    for i in range(6, -1, -1):  # От 6 дней назад до сегодня
        date = timezone.now().date() - timedelta(days=i)
        visits = PageVisit.objects.filter(visited_at__date=date).count()
        daily_visits.append({
            'date': date.strftime('%d.%m'),
            'visits': visits
        })
    
    # Последние посещения
    recent_visits = PageVisit.objects.select_related('user').order_by('-visited_at')[:20]
    
    context = {
        'total_visits': total_visits,
        'visits_last_30_days': visits_last_30_days,
        'unique_visitors': unique_visitors,
        'popular_pages': popular_pages,
        'daily_visits': daily_visits,
        'recent_visits': recent_visits,
    }
    
    return render(request, 'admin/analytics.html', context)

@staff_member_required
def export_analytics(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="analytics.csv"'
    
    # Добавляем BOM для корректного отображения кириллицы в Excel
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow(['URL', 'IP адрес', 'Пользователь', 'Дата посещения', 'User Agent'])
    
    visits = PageVisit.objects.select_related('user').order_by('-visited_at')
    for visit in visits:
        writer.writerow([
            visit.page_url,
            visit.ip_address,
            visit.user.username if visit.user else 'Анонимный',
            visit.visited_at.strftime('%Y-%m-%d %H:%M:%S'),
            visit.user_agent[:100]  # Ограничиваем длину
        ])
    
    return response
