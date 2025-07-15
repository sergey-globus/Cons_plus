from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultation/', views.consultation, name='consultation'),
    path('documents/', views.document_generator, name='document_generator'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-word/', views.download_word, name='download_word'),
    path('legal-news/', views.legal_news, name='legal_news'),
    path('reference-materials/', views.reference_materials, name='reference_materials'),
    path('marketplace-rights/', views.marketplace_rights, name='marketplace_rights'),
    path('order-cancellation/', views.order_cancellation, name='order_cancellation'),
    path('price-error/', views.price_error, name='price_error'),
    path('glossary/', views.glossary, name='glossary'),
    path('template/preview/<int:template_id>/', views.preview_template, name='preview_template'),
]
