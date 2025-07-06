from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    passport_number = models.CharField(max_length=20, blank=True, verbose_name="Номер паспорта")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Возраст")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"

    def get_full_name(self):
        """Получить полное имя пользователя"""
        parts = [self.user.last_name, self.user.first_name, self.middle_name]
        return " ".join(part for part in parts if part)

# Автоматическое создание профиля при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
