from django.urls import path
from . import views

app_name = 'legal_api'

urlpatterns = [
    path('news/', views.get_legal_news, name='get_legal_news'),
    path('search/', views.search_legal_info, name='search_legal_info'),
    path('template/<int:template_id>/fields/', views.get_template_fields, name='get_template_fields'),
    path('documents/preview/', views.preview_document, name='preview_document'),
]
