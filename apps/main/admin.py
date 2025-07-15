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
    list_display = ('first_name', 'last_name', 'email', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
