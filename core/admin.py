from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Blog, Campaign, Service, Appointment, Patient, SessionNote

# --- BUTONLARI ÜRETEN SİHİRLİ ŞABLON ---
class ButonluAdmin(admin.ModelAdmin):
    def islemler(self, obj):
        # Hangi modeldeysek (Blog, Randevu vs.) onun düzenleme ve silme linkini otomatik bulur
        opts = self.model._meta
        duzenle_url = reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[obj.pk])
        sil_url = reverse(f'admin:{opts.app_label}_{opts.model_name}_delete', args=[obj.pk])
        
        # Sibel Yeşili ve Kırmızı şık butonlar oluşturur
        return format_html(
            '<a class="btn" style="background-color: #79aba1; color: white; padding: 5px 15px; font-size: 12px; border-radius: 20px; font-weight: 600;" href="{}">✎ Düzenle</a>&nbsp;&nbsp;'
            '<a class="btn" style="background-color: #d96c6c; color: white; padding: 5px 15px; font-size: 12px; border-radius: 20px; font-weight: 600;" href="{}">🗑️ Sil</a>',
            duzenle_url, sil_url
        )
    islemler.short_description = 'Hızlı İşlemler' # Tablonun en sağındaki sütunun adı

# --- MODELLERİMİZİ SİSTEME KAYDEDİYORUZ ---

@admin.register(Blog)
class BlogAdmin(ButonluAdmin):
    list_display = ('title', 'created_at', 'is_active', 'islemler') # Tabloda görünecek sütunlar

@admin.register(Appointment)
class AppointmentAdmin(ButonluAdmin):
    list_display = ('client_name', 'date', 'time', 'status', 'islemler')
    list_filter = ('status', 'date') # Yan tarafa filtreleme koyar

@admin.register(Patient)
class PatientAdmin(ButonluAdmin):
    list_display = ('full_name', 'phone', 'first_session_date', 'islemler')

@admin.register(Service)
class ServiceAdmin(ButonluAdmin):
    list_display = ('title', 'is_active', 'islemler')

@admin.register(Campaign)
class CampaignAdmin(ButonluAdmin):
    list_display = ('title', 'is_active', 'islemler')