from django.contrib import admin
from django.contrib import messages # YAPAY ZEKA MESAJLARI İÇİN EKLEDİK
from django.utils.html import format_html
from django.urls import reverse
from .models import Blog, Campaign, Service, Appointment, Patient, SessionNote, ContactMessage
from .ai_utils import analiz_et_gemini # YAPAY ZEKA BEYNİMİZ

# --- BUTONLARI ÜRETEN SİHİRLİ ŞABLON (SENİN EFSANE TASARIMIN) ---
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
    islemler.short_description = 'Hızlı İşlemler'

# --- MODELLERİMİZİ SİSTEME KAYDEDİYORUZ ---

@admin.register(Blog)
class BlogAdmin(ButonluAdmin):
    list_display = ('title', 'created_at', 'is_active', 'islemler')

@admin.register(Appointment)
class AppointmentAdmin(ButonluAdmin):
    list_display = ('client_name', 'date', 'time', 'status', 'islemler')
    list_filter = ('status', 'date')

@admin.register(Service)
class ServiceAdmin(ButonluAdmin):
    list_display = ('title', 'is_active', 'islemler')

@admin.register(Campaign)
class CampaignAdmin(ButonluAdmin):
    list_display = ('title', 'is_active', 'islemler')

# SİBEL HANIM NOT GİREBİLSİN DİYE BUNU DA EKLİYORUZ
@admin.register(SessionNote)
class SessionNoteAdmin(ButonluAdmin):
    list_display = ('client_name', 'created_at', 'islemler')
    search_fields = ('client_name',)

# --- VE İŞTE ŞAMPİYONLAR LİGİ: YAPAY ZEKA DESTEKLİ DANIŞAN PANELİ ---
@admin.register(Patient)
class PatientAdmin(ButonluAdmin):
    list_display = ('full_name', 'phone', 'first_session_date', 'islemler')
    search_fields = ('full_name', 'phone')
    actions = ['generate_ai_summary'] # SİHİRLİ BUTON

    @admin.action(description='✨ Yapay Zeka ile Vaka Özeti Çıkar')
    def generate_ai_summary(self, request, queryset):
        for patient in queryset:
            # 1. Hastanın ismine ait tüm seans notlarını eskiden yeniye doğru getir
            notes = SessionNote.objects.filter(client_name=patient.full_name).order_by('created_at')
            
            if not notes.exists():
                self.message_user(request, f"Uyarı: {patient.full_name} için hiç seans notu bulunamadı.", level=messages.WARNING)
                continue
            
            # 2. Notları birleştir (Sadece "1. Seans: ... 2. Seans: ..." şeklinde, gizliliğe uygun)
            combined_notes = ""
            for i, note in enumerate(notes, 1):
                tarih = note.created_at.strftime('%d.%m.%Y')
                combined_notes += f"\n--- {i}. Seans ({tarih}) ---\n{note.note}\n"
            
            # 3. Gemini'ye yolla ve analizi al
            ai_result = analiz_et_gemini(combined_notes)
            
            # 4. Gelen efsane özeti hastanın "Genel Değerlendirme" kısmına kaydet
            patient.summary = ai_result
            patient.save()
            
            self.message_user(request, f"✨ {patient.full_name} isimli danışanın vaka özeti yapay zeka ile başarıyla oluşturuldu!", level=messages.SUCCESS)