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
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'created_at')
    readonly_fields = ('get_first_name', 'get_last_name', 'get_email')
    
    def get_first_name(self, obj):
        return obj.first_name
    get_first_name.short_description = 'Имя'
    
    def get_last_name(self, obj):
        return obj.last_name
    get_last_name.short_description = 'Фамилия'
    
    def get_email(self, obj):
        return obj.email
    get_email.short_description = 'Email'

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
