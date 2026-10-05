"""
Django settings for core project.
"""

from pathlib import Path

import dj_database_url
from decouple import Csv, config
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-vheri7b@%*p(36s9_fioa0y6tc6c$%5vv&-*ci)rza8!^i#jn+",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

# Render, sitenin adresini (ör. str-web.onrender.com) bu değişkene kendisi
# yazar. Elle ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS'e eklemeye gerek kalmasın diye
# burada otomatik ekliyoruz.
RENDER_EXTERNAL_HOSTNAME = config("RENDER_EXTERNAL_HOSTNAME", default="")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# Render HTTPS'i kendi proxy'sinde sonlandırıp Django'ya düz HTTP iletiyor.
# Bu olmadan Django isteği güvensiz sanıyor ve admin girişi gibi POST
# formları "CSRF verification failed – Origin checking failed" ile reddediliyor.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Application definition

INSTALLED_APPS = [
    # modeltranslation, admin'i patch'lediği için django.contrib.admin'den
    # önce yüklenmeli.
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "tailwind",
    "theme",
    "django_browser_reload",
    "cloudinary_storage",
    "cloudinary",
    # Local
    "catalog",
    "icerik",
]

TAILWIND_APP_NAME = "theme"

# Only used by django-tailwind's live-reload dev server.
INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "catalog.context_processors.navbar_markalar",
                "catalog.context_processors.navbar_kategoriler",
                "icerik.context_processors.site_ayarlari",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#
# DATABASE_URL, sağlanan bir Supabase Postgres bağlantı dizesidir, ör:
# postgres://<user>:<password>@<host>:5432/postgres
# Yerel geliştirmede .env dosyasında tanımlı değilse sqlite'a düşer.

DATABASES = {
    # dj_database_url.config() kendi başına os.environ'a bakar; python-decouple
    # ise .env dosyasını os.environ'a yazmaz, sadece kendi config() çağrıları
    # için okur. İkisi birlikte kullanılınca DATABASE_URL .env'e yazılsa bile
    # sessizce görmezden geliniyordu (proje hep SQLite'a düşüyordu). Bunun
    # yerine .env'i decouple ile okuyup dj_database_url.parse()'a veriyoruz.
    "default": dj_database_url.parse(
        config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "tr"

LANGUAGES = [
    ("tr", "Türkçe"),
    ("en", "English"),
    ("fr", "Français"),
    ("es", "Español"),
    ("ar", "العربية"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# django-modeltranslation — veritabanı içeriğini (ürün/kategori adı ve
# açıklaması) çok dilli yapmak için. Şablon metinleri için kullanılan
# yukarıdaki LANGUAGES/gettext sisteminden ayrı bir mekanizma: bu, model
# alanlarını dile göre ayrı kolonlara böler (ör. ad_tr, ad_en, ...).
MODELTRANSLATION_DEFAULT_LANGUAGE = "tr"
MODELTRANSLATION_LANGUAGES = ("tr", "en", "fr", "es", "ar")

TIME_ZONE = "Europe/Istanbul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "assets", BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (product images). Production'da (hosting platformunun dosya
# sistemi geçici olduğu için) Cloudinary kullanılır. Yerelde CLOUDINARY_*
# değişkenleri boşsa (Cloudinary hesabı gerekmesin diye) düz dosya sistemine
# (MEDIA_ROOT) düşer — aksi halde admin'den herhangi bir görsel yüklemek
# "Must supply api_key" hatasıyla çöker.
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY": config("CLOUDINARY_API_KEY", default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
}

if CLOUDINARY_STORAGE["CLOUD_NAME"]:
    DEFAULT_MEDIA_BACKEND = "cloudinary_storage.storage.MediaCloudinaryStorage"
elif DEBUG:
    DEFAULT_MEDIA_BACKEND = "django.core.files.storage.FileSystemStorage"
else:
    # Production'da sessizce diske düşmek, yüklenen görsellerin bir sonraki
    # deploy'da kaybolması (ve DEBUG=False'ta hiç sunulmaması) demek —
    # ford logosunun kaybolmasının sebebi de bu tür bir sessiz geçişti.
    raise ImproperlyConfigured(
        "DEBUG=False iken CLOUDINARY_CLOUD_NAME/API_KEY/API_SECRET tanımlı olmalı."
    )

STORAGES = {
    "default": {
        "BACKEND": DEFAULT_MEDIA_BACKEND,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
