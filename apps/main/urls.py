from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultation/', views.consultation, name='consultation'),
    path('documents/', views.document_generator, name='document_generator'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('legal-news/', views.legal_news, name='legal_news'),
    path('reference/', views.reference_materials, name='reference_materials'),
    path('news/platform-economy/', views.platform_economy_news_detail, name='platform_economy_news_detail'),
    path('news/platform-economy_2/', views.platform_economy_news_detail_2, name='platform_economy_news_detail_2'),

    path('reference/return/', views.return_category, name='return_category'),
    path('reference/seller/', views.seller_category, name='seller_category'),
    path('reference/delivery/', views.delivery_category, name='delivery_category'),

    path('marketplace-rights/', views.marketplace_rights, name='marketplace-rights'),
    path('order-cancellation/', views.order_cancellation, name='order-cancellation'),
    path('price-error/', views.price_error, name='price-error'),
    path('art1/', views.bad_goods_delivered, name='art1'),
    path('art2/', views.dosydebnii_isk, name='art2'),
    path('art3/', views.isk_zyavlenie, name='art3'),
    path('art4/', views.return_bad, name='art4'),
    path('art5/', views.return_good, name='art5'),
    path('art7/', views.return_nevozvrat, name='art7'),
    path('art8/', views.return_plata, name='art8'),
    path('art9/', views.return_vskr_ypakovka, name='art9'),
    path('art10/', views.wrong_price, name='art10'),
    path('pretnezya/', views.pretnezya, name='pretnezya'),

    path('glossary/', views.glossary, name='glossary'),
    path('template/preview/<int:template_id>/', views.preview_template, name='preview_template'),
    path('download-empty-template/<int:template_id>/', views.download_empty_template, name='download_empty_template'),
    path('document_result/<int:template_id>/', views.document_result, name='document_result'),
    path('download_word/<int:template_id>/', views.download_word, name='download_word'),
    path('download-empty-template-pdf/<int:template_id>/', views.download_empty_template_pdf, name='download_empty_template_pdf'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
]
