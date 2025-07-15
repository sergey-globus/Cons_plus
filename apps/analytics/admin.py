from django.contrib import admin
from .models import PageVisit

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('page_url', 'user', 'ip_address', 'visited_at')
    list_filter = ('visited_at',)
    search_fields = ('page_url', 'user__username', 'ip_address')
    readonly_fields = ('visited_at',)
    
    def has_add_permission(self, request):
        return False  # Запрещаем добавление через админку
