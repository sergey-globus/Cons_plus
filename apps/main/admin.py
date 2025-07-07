from django.contrib import admin
from .models import FAQ, Consultation, DocumentTemplate

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

from django.contrib import admin
from .models import LegalNews

@admin.register(LegalNews)
class LegalNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic_display', 'published_at', 'is_published', 'author')
    list_filter = ('is_published', 'topic', 'published_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    readonly_fields = ('published_at', 'author')
    
    def topic_display(self, obj):
        return obj.get_topic_display()
    topic_display.short_description = 'Тема'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)