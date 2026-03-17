from django.db import models
from django.utils import timezone # BUNU EN ÜSTE EKLE

# --- SİTE İÇERİKLERİ ---

class Campaign(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kampanya Başlığı")
    description = models.TextField(blank=True, verbose_name="Açıklama (Opsiyonel)")
    image = models.ImageField(upload_to='campaigns/%Y/%m/', verbose_name="Kampanya Görseli")
    link = models.URLField(blank=True, verbose_name="Tıklanınca Gideceği Link")
    is_active = models.BooleanField(default=True, verbose_name="Yayında mı?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kampanya"
        verbose_name_plural = "Kampanyalar"

    def __str__(self):
        return self.title


class Service(models.Model):
    ICON_CHOICES = [
        ('fas fa-couch', '🛋️ Terapi Koltuğu (Bireysel)'),
        ('fas fa-users', '👥 Çift / Grup Terapisi'),
        ('fas fa-child', '🧸 Çocuk / Ergen Terapisi'),
        ('fas fa-brain', '🧠 Bilişsel / Beyin'),
        ('fas fa-laptop', '💻 Online Terapi'),
    ]

    title = models.CharField(max_length=100, verbose_name="Hizmet Başlığı")
    description = models.TextField(verbose_name="Kısa Açıklama")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fas fa-couch')
    is_active = models.BooleanField(default=True, verbose_name="Yayında mı?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hizmet"
        verbose_name_plural = "Hizmetler"

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Blog Başlığı")
    short_description = models.TextField(verbose_name="Kısa Açıklama (Önizleme)", max_length=300)
    content = models.TextField(verbose_name="İçerik (Uzun Yazı)")
    image = models.ImageField(upload_to='blog_images/', verbose_name="Kapak Resmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Yayında mı?")

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# --- KLİNİK YÖNETİMİ (SİBEL HANIM'IN PANELİ İÇİN) ---

class Appointment(models.Model):
    TIME_SLOTS = [
        ('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'),
        ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'),
    ]

    STATUS_CHOICES = [
        ('pending', '⏳ Bekliyor'),
        ('confirmed', '✅ Onaylandı'),
        ('completed', '🏁 Tamamlandı'),
        ('cancelled', '❌ İptal Edildi'),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Danışan Adı")
    client_email = models.EmailField(verbose_name="E-posta")
    client_phone = models.CharField(max_length=20, verbose_name="Telefon")
    service = models.CharField(max_length=100, verbose_name="Hizmet", blank=True)
    date = models.DateField(verbose_name="Randevu Tarihi")
    time = models.CharField(max_length=10, choices=TIME_SLOTS, verbose_name="Randevu Saati")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, verbose_name="Not")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Randevu"
        verbose_name_plural = "Randevular"
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.client_name} - {self.date} {self.time}"


class Patient(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Danışan Adı Soyadı")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True)
    first_session_date = models.DateField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    summary = models.TextField(blank=True, verbose_name="Genel Değerlendirme")

    class Meta:
        verbose_name = "Danışan"
        verbose_name_plural = "Danışanlar"

    def __str__(self):
        return self.full_name


class SessionNote(models.Model):
    client_name = models.CharField(max_length=200, verbose_name="Danışan Adı")
    note = models.TextField(verbose_name="Seans Notu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")

    def __str__(self):
        return f"{self.client_name} - {self.created_at.strftime('%d.%m.%Y')}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Gönderen Adı")
    email = models.EmailField(verbose_name="E-Posta")
    message = models.TextField(verbose_name="Mesaj İçeriği")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")
class SessionNote(models.Model):
    # null=True, blank=True ekledik ki geçmiş kayıtlar için sorun çıkarmasın
    client_name = models.CharField(max_length=200, verbose_name="Danışan Adı", null=True, blank=True)
    note = models.TextField(verbose_name="Seans Notu")
    # auto_now_add yerine timezone.now kullandık ki hata vermesin
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Tarih")

    def __str__(self):
        return f"{self.client_name} - {self.created_at.strftime('%d.%m.%Y')}"
    def __str__(self):
        return f"{self.name} - {self.email}"    