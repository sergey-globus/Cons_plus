from django.urls import path
from . import views
from .views import news_detail
from .views import add_news_redirect

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq_list, name='faq'),
    path('consultation/', views.consultation, name='consultation'),
    path('documents/', views.document_generator, name='document_generator'),
    path('legal-news/', views.legal_news, name='legal_news'),
    path('admin-legal-news/', views.admin_legal_news, name='admin_legal_news'),
    path('admin-add-news/', views.admin_add_news, name='admin_add_news'),
    path('admin/toggle-news-status/<int:news_id>/', views.toggle_news_status, name='toggle_news_status'),
    path('legal-news/<int:pk>/', news_detail, name='news_detail'),
    path('add-news/', add_news_redirect, name='add_news'),
]
