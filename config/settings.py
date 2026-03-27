from pathlib import Path
from dotenv import load_dotenv
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'yedek-guvenlik-anahtari')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']
# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization (Türkçe ve Türkiye Saati)
LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
# YENİ EKLENEN: Django'ya kök dizindeki static klasörünü gösteriyoruz
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- JAZZMIN (ADMİN PANELİ) AYARLARI ---
JAZZMIN_SETTINGS = {
    "site_title": "Psk. Sibel D. Yönetim",
    "site_header": "Sibel Domdomoğulları",
    "site_brand": "Klinik Yönetimi",
    "welcome_sign": "Klinik Yönetim Paneline Hoş Geldiniz",
    "copyright": "Psk. Sibel Domdomoğulları",
    
    "custom_css": "admin_klinik.css", 
    "show_ui_builder": False, 
    "hide_models": ["auth.group"],
    
    # --- İŞTE BURASI! TÜM LİNKLERİ SİTE GİBİ ÜST MENÜYE ALIYORUZ ---
    "search_model": [], # Üstteki kaba arama çubuğunu gizledik
    "topmenu_links": [
        {"name": "Klinik Anasayfa",  "url": "admin:index"},
        {"model": "core.Appointment", "name": "Randevular"},
        {"model": "core.Blog", "name": "Blog Yazıları"},
        {"model": "core.Service", "name": "Hizmetler"},
        {"model": "core.Campaign", "name": "Kampanyalar"},
        {"name": "Siteyi Görüntüle ↗", "url": "/", "new_window": True},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "litera", 
}
load_dotenv() # KASAYI AÇTIK
# Mail Ayarları (Eksik tırnak düzeltildi)
# --- GERÇEK MAİL GÖNDERME AYARLARI ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'Klinik Pro <>'