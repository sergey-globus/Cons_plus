from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultation/', views.consultation, name='consultation'),
    path('documents/', views.document_generator, name='document_generator'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-word/', views.download_word, name='download_word'),
    path('legal-news/', views.legal_news, name='legal_news'),
    path('reference/', views.reference_materials, name='reference_materials'),
    path('reference/price/', views.price_category, name='price_category'),
    path('reference/return/', views.return_category, name='return_category'),
    path('reference/seller/', views.seller_category, name='seller_category'),
    path('marketplace-rights/', views.marketplace_rights, name='marketplace_rights'),
    path('order-cancellation/', views.order_cancellation, name='order_cancellation'),
    path('price-error/', views.price_error, name='price_error'),
    path('reference/delivery/', views.delivery_category, name='delivery_category'),
    path('reference/damaged/', views.damaged_category, name='damaged_category'),
    path('reference/delivery-terms/', views.delivery_terms_category, name='delivery_terms_category'),
    path('glossary/', views.glossary, name='glossary'),
    path('template/preview/<int:template_id>/', views.preview_template, name='preview_template'),
    path('download-empty-template/<int:template_id>/', views.download_empty_template, name='download_empty_template'),
]
