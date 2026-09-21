# OTOPARÇA — Araç Yedek Parça Katalog Sitesi

Araç yedek parçası satan bir firma için ürün kataloğu ve tanıtım (vitrin)
web sitesi. Bu aşamada amaç, ürünleri veritabanından gösteren tam bir
e-ticaret sitesi değil; firmanın ürün ve iletişim bilgilerini sergileyen,
ilerleyen fazlarda katalog verisiyle beslenecek bir temel altyapı kurmaktır.

## Teknoloji Yığını

| Katman | Teknoloji |
|---|---|
| Backend | Python, Django |
| Önyüz (Frontend) | Django Templates + Tailwind CSS (`django-tailwind`) |
| Veritabanı | PostgreSQL |
| Medya (ürün görselleri) | Cloudinary |
| Ortam değişkenleri | `python-decouple` |

## Nerede Barınıyor?

| Bileşen | Platform |
|---|---|
| Kod / Web sunucusu | Render.com veya Railway.app |
| Veritabanı (PostgreSQL) | Supabase |
| Ürün görselleri / medya dosyaları | Cloudinary |

Render ve Railway gibi platformlarda dosya sistemi geçicidir (her
deploy'da sıfırlanır); bu yüzden kullanıcı tarafından yüklenen ürün
görselleri sunucuda değil, Cloudinary üzerinde saklanır. Statik dosyalar
(CSS/JS) ise `whitenoise` ile doğrudan Django üzerinden servis edilir.

## Proje Yapısı

```
str-web/
├── core/          # Django proje ayarları (settings, urls, wsgi)
├── catalog/       # Ana uygulama: sayfalar, (ilerleyen fazda) ürün modelleri
├── theme/         # django-tailwind tarafından üretilen Tailwind uygulaması
├── templates/      # Proje geneli şablonlar (base.html)
├── assets/         # Proje geneli statik dosyalar (STATICFILES_DIRS)
├── requirements.txt
├── .env.example
├── PLAN.md
└── README.md
```

## Yerel Kurulum

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # gerekli değerleri doldurun

python manage.py migrate
python manage.py tailwind start # ayrı bir terminalde: Tailwind watch modu
python manage.py runserver      # ana terminalde: Django dev sunucusu
```

Site varsayılan olarak http://127.0.0.1:8000 adresinde çalışır.

## Ortam Değişkenleri (.env)

Detaylar için `.env.example` dosyasına bakın:

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` — Django temel ayarları
- `DATABASE_URL` — Supabase PostgreSQL bağlantı dizesi (boş bırakılırsa
  yerelde otomatik olarak SQLite kullanılır)
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` —
  Cloudinary medya depolama bilgileri

## Yol Haritası

Fazlara ayrılmış detaylı plan için [`PLAN.md`](./PLAN.md) dosyasına bakın.
