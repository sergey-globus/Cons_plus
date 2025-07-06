from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq_list, name='faq'),
    path('consultation/', views.consultation, name='consultation'),
    path('documents/', views.document_generator, name='document_generator'),
    path('legal-news/', views.legal_news, name='legal_news'),
]
