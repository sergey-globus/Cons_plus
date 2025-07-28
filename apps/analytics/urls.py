from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.analytics_dashboard, name='analytics_dashboard'),
    path('export/', views.export_analytics, name='export_analytics'),
]
