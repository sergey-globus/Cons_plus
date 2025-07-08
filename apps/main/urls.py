from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultation/', views.consultation, name='consultation'),
    path('documents/', views.document_generator, name='document_generator'),
    path('legal-news/', views.legal_news, name='legal_news'),
    path('reference-materials/', views.reference_materials, name='reference_materials'),
    path('marketplace-rights/', views.marketplace_rights, name='marketplace_rights'),
]
