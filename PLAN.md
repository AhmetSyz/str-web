# Proje Planı

Bu belge, projenin ilerleyeceği fazları kabaca özetler. Her fazın
detaylı görev dökümü, o faza başlanmadan hemen önce ayrıca çıkarılacaktır.

## Faz 1: Kurulum ve Temel Şablonlar

- Django projesi (`core`) ve ana uygulamanın (`catalog`) oluşturulması
- `django-tailwind` entegrasyonu
- Temel şablonlar: `base.html` (Navbar + Footer), `index.html` (Anasayfa),
  `iletisim.html` (İletişim)
- Veritabanı sorgusu içermeyen, statik Anasayfa ve İletişim view'ları

## Faz 2: Veritabanı Modelleri

- Ürün, kategori ve araç eşleştirme (uyumluluk) modellerinin tasarımı
- Cloudinary ile ürün görseli yükleme entegrasyonu
- Admin panel üzerinden içerik yönetimi

---

Sonraki fazlar (ürün listeleme/filtreleme sayfaları, arama, deploy
yapılandırması vb.) Faz 2 tamamlandıktan sonra ayrıca planlanacaktır.
