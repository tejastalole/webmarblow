from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_nsc1=9r81a2_sv_&6mt85^4!@6o1=@fc3zm^h$-$c58r!n=sn'

# DEBUG = True
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']
# Remove empty strings from ALLOWED_HOSTS
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'webmarblow',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webmarblow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'website' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.company',
            ],
        },
    },
]

WSGI_APPLICATION = 'webmarblow.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Database configuration
# Use environment variable for database URL if available (for Render PostgreSQL)
# Otherwise, fall back to SQLite
# On Render, use /tmp for SQLite to ensure write permissions
db_path = os.environ.get('DATABASE_URL')
if db_path:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                default=db_path,
                conn_max_age=600,
                ssl_require=True
            )
        }
    except ImportError:
        # Fallback if dj_database_url is not available
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
else:
    # For Render free tier, use /tmp directory for SQLite
    # This ensures write permissions
    # Check if we're on Render by checking for RENDER environment or hostname
    is_render = os.environ.get('RENDER') or 'onrender.com' in os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
    if is_render:
        db_file = '/tmp/db.sqlite3'
    else:
        db_file = os.path.join(BASE_DIR, 'db.sqlite3')
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_file,
        }
    }



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Quote/contact leads are emailed here.
LEAD_NOTIFY_EMAIL = os.environ.get('LEAD_NOTIFY_EMAIL', 'tejastalole7@gmail.com')
SITE_URL = os.environ.get('SITE_URL', 'https://webmarblow.vercel.app')

# Gmail SMTP: set EMAIL_HOST_USER + EMAIL_HOST_PASSWORD (App Password) on Vercel.
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
    if os.environ.get('EMAIL_HOST_PASSWORD')
    else 'django.core.mail.backends.console.EmailBackend',
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'tejastalole7@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

COMPANY = {
    'name': 'WebMarblow',
    'tagline': 'IDEAS · WEBSITES · GROWTH',
    'slogan': 'Your Digital Growth Partner',
    'closing': 'Websites Today, Bigger Tomorrows',
    'email': 'tejastalole7@gmail.com',
    'website': 'www.webmarblow.com',
    'phone': '+91 98765 43210',
    'address': 'Pune, Maharashtra, India',
    'hours': 'Mon - Sat, 10:00 AM - 7:00 PM IST',
}


# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'product_list'
LOGOUT_REDIRECT_URL = 'login'