from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.mail import send_mail
import json

from .models import Campaign, Service, Appointment, Blog, Patient, SessionNote, ContactMessage

# --- SİTE ÖNYÜZÜ ---
def index(request):
    return render(request, 'index.html', {
        'campaigns': Campaign.objects.filter(is_active=True).order_by('-created_at'),
        'services': Service.objects.filter(is_active=True).order_by('created_at'),
        'latest_blogs': Blog.objects.filter(is_active=True)[:3],
    })

def about(request): return render(request, 'about.html')
def blog_list(request): return render(request, 'blog_list.html', {'blogs': Blog.objects.filter(is_active=True)})
def service_detail(request, pk): return render(request, 'service_detail.html', {'service': get_object_or_404(Service, pk=pk)})

def appointment(request):
    if request.method == 'POST':
        Appointment.objects.create(
            client_name=request.POST.get('name'), client_email=request.POST.get('email'),
            client_phone=request.POST.get('phone'), service=request.POST.get('service'),
            date=request.POST.get('date'), time=request.POST.get('time'), message=request.POST.get('message')
        )
        messages.success(request, "Başvurunuz alındı. Onay durumunda mail iletilecektir.")
        return redirect('appointment')
    return render(request, 'appointment.html', {'services': Service.objects.filter(is_active=True)})

def get_available_hours(request):
    date_str = request.GET.get('date')
    taken_slots = Appointment.objects.filter(date=date_str, status='confirmed').values_list('time', flat=True)
    all_slots = [('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00')]
    return JsonResponse({'slots': [{'value': c, 'label': l} for c, l in all_slots if c not in taken_slots]})

# --- KLİNİK PRO DASHBOARD ---
@staff_member_required
def custom_dashboard(request, tab='genel'):
    bugun = timezone.now().date()
    
    # VERİLER
    bekleyenler = Appointment.objects.filter(status='pending').order_by('-created_at')
    tarihsiz_onaylilar = Appointment.objects.filter(status='approved_pending_date').order_by('-created_at') # YENİ: Pasif Onaylılar
    yaklasan_seanslar = Appointment.objects.filter(status='confirmed', date__gte=bugun).order_by('date', 'time')
    gunun_randevulari = Appointment.objects.filter(date=bugun, status='confirmed').order_by('time')
    onayli_isimler = set(Appointment.objects.filter(status='confirmed').values_list('client_name', flat=True))

    context = {
        'active_tab': tab,
        'toplam_danisan': Patient.objects.count(),
        'bekleyen_randevular': bekleyenler,
        'tarihsiz_onaylilar': tarihsiz_onaylilar, # Takvimde uyarı verecek kısım
        'yaklasan_seanslar': yaklasan_seanslar,
        'gunun_randevulari': gunun_randevulari,
        'onayli_isimler': onayli_isimler,
        'siradaki_seans': gunun_randevulari.filter(time__gte=timezone.now().strftime("%H:%M")).first(),
        'gelen_mesajlar': ContactMessage.objects.all().order_by('-created_at'),
        'bloglar': Blog.objects.all().order_by('-created_at'),
        'now': timezone.now(),
    }
    return render(request, 'klinik_pro.html', context)

# 1. BAŞVURU İNCELEME VE İŞLEM YAPMA (MODAL'DAN GELEN VERİ)
@staff_member_required
def randevu_islem_post(request):
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        islem = request.POST.get('islem')
        randevu = get_object_or_404(Appointment, pk=app_id)
        
        if islem == 'onayla_tarihli':
            # Hem onayladı hem tarih verdi -> Mail gider
            randevu.date = request.POST.get('date')
            randevu.time = request.POST.get('time')
            randevu.status = 'confirmed'
            send_mail('Randevunuz Onaylandı - Psk. Sibel', f"Merhaba {randevu.client_name},\n\n{randevu.date} saat {randevu.time} randevunuz onaylanmıştır.", 'bilgi@psksibelsiten.com', [randevu.client_email], fail_silently=False)
        
        elif islem == 'onayla_tarihsiz':
            # Sadece onayladı, tarih vermedi -> Mail GİTMEZ, pasife düşer
            randevu.status = 'approved_pending_date'
            
        elif islem == 'reddet':
            randevu.status = 'cancelled'
            send_mail('Randevu Bilgilendirme - Psk. Sibel', f"Merhaba {randevu.client_name},\n\nÜzülerek belirtiriz ki yoğunluktan dolayı talebiniz iptal edilmiştir.", 'bilgi@psksibelsiten.com', [randevu.client_email], fail_silently=True)
            
        randevu.save()
    return redirect('custom_dashboard_tab', tab='danisanlar')

# 2. PASİF HASTALARA SONRADAN TARİH ATAMA
@staff_member_required
def tarih_ata(request):
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        randevu = get_object_or_404(Appointment, pk=app_id)
        randevu.date = request.POST.get('date')
        randevu.time = request.POST.get('time')
        randevu.status = 'confirmed' # Artık onaylandı
        randevu.save()
        # Şimdi maili atıyoruz
        send_mail('Randevu Saatiniz Belirlendi - Psk. Sibel', f"Merhaba {randevu.client_name},\n\nRandevunuz {randevu.date} saat {randevu.time} olarak belirlenmiştir.", 'bilgi@psksibelsiten.com', [randevu.client_email], fail_silently=True)
    return redirect('custom_dashboard_tab', tab='seans_takvimi')

# 3. YENİ DEVAM SEANSI EKLEME
@staff_member_required
def yeni_seans_ekle(request):
    if request.method == 'POST':
        Appointment.objects.create(
            client_name=request.POST.get('client_name'), service='Devam Seansı',
            date=request.POST.get('date'), time=request.POST.get('time'), status='confirmed'
        )
    return redirect('custom_dashboard_tab', tab='seans_takvimi')

# API'LER (AJAX İÇİN)
@staff_member_required
def get_appointments_api(request):
    data = [{'id': r.id, 'client_name': r.client_name, 'client_email': r.client_email, 'service': r.service, 'date': str(r.date), 'time': str(r.time), 'message': r.message or "Mesaj/Şikayet belirtilmedi."} for r in Appointment.objects.filter(status='pending').order_by('-created_at')]
    return JsonResponse({'appointments': data})

@staff_member_required
def get_messages_api(request):
    data = [{'id': m.id, 'name': m.name, 'email': m.email, 'message': m.message, 'time': m.created_at.strftime("%H:%M")} for m in ContactMessage.objects.all().order_by('-created_at')[:20]]
    return JsonResponse({'messages': data})
# YENİ: Seans Bitirme ve Not Kaydetme Motoru
@staff_member_required
def seans_bitir(request):
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        note_text = request.POST.get('note') # Textarea'dan gelen not
        
        # Sadece notu kaydediyoruz (Tarih sormuyoruz)
        SessionNote.objects.create(
            client_name=client_name, 
            note=note_text
        )
        
        # (İsteğe bağlı) Eğer randevuyu "Tamamlandı" yapmak istersen ileride buraya kod ekleriz
        
    return redirect('custom_dashboard_tab', tab='seans_odasi')
@staff_member_required
def seans_bitir(request):
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        note_text = request.POST.get('note') # Textarea'dan gelen yazıyı yakalar
        
        # Sadece notu kaydediyoruz
        SessionNote.objects.create(
            client_name=client_name, 
            note=note_text
        )
        
    return redirect('custom_dashboard_tab', tab='seans_odasi')
@staff_member_required
def get_patient_notes_api(request):
    client_name = request.GET.get('client_name')
    # Hastanın geçmiş notlarını eskiden yeniye doğru sırala
    gecmis_notlar = SessionNote.objects.filter(client_name=client_name).order_by('id')
    
    data = []
    for index, not_kaydi in enumerate(gecmis_notlar):
        data.append({
            'seans_no': index + 1,
            'not_icerigi': not_kaydi.note,
            # Eğer SessionNote modelinde 'created_at' tarihi yoksa patlamaması için basit bir try-except
            'tarih': getattr(not_kaydi, 'created_at', timezone.now()).strftime("%d.%m.%Y")
        })
    
    siradaki_seans_no = gecmis_notlar.count() + 1
    
    return JsonResponse({
        'notes': data, 
        'next_session': siradaki_seans_no
    })
