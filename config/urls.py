from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views 
import os
urlpatterns = [
    # API'LER (AJAX İÇİN)
    path('admin/api/messages/', views.get_messages_api, name='get_messages_api'),
    path('admin/api/appointments/', views.get_appointments_api, name='get_appointments_api'),
    path('admin/api/notes/', views.get_patient_notes_api, name='get_patient_notes_api'),
    # İŞLEM YOLLARI (YENİ)
    path('admin/randevu-islem-post/', views.randevu_islem_post, name='randevu_islem_post'),
    path('admin/tarih-ata/', views.tarih_ata, name='tarih_ata'),
    path('admin/yeni-seans/', views.yeni_seans_ekle, name='yeni_seans_ekle'),
    path('admin/seans-bitir/', views.seans_bitir, name='seans_bitir'), # NOT KAYDETME YOLU
    path('admin/seans-bitir/', views.seans_bitir, name='seans_bitir'),
    # DASHBOARD
    path('klinik/', views.custom_dashboard, name='custom_dashboard'),
    path('admin/dashboard/<str:tab>/', views.custom_dashboard, name='custom_dashboard_tab'),
    path('admin/', admin.site.urls),
    
    # SİTE YOLLARI
    path('', views.index, name='index'),
    path('hakkimda/', views.about, name='about'),
    path('randevu/', views.appointment, name='appointment'),
    path('blog/', views.blog_list, name='blog_list'),
    path('terapi/<int:pk>/', views.service_detail, name='service_detail'),
    path('api/get-hours/', views.get_available_hours, name='get_available_hours'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)