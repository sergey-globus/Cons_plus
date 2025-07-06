from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Перерегистрируем User модель
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'middle_name', 'phone', 'age', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('created_at',)
