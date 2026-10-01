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

## Faz 3: Ürün Kataloğu Ön Yüzü (Frontend)

Navbar mega-menu referansı: `str-web/navbar example.png`.

- [x] Navbar'daki "Ürünler" dropdown'ı (statik "Kategori 1/2/3") kaldırılıp
      **Kategoriler** için düz bir sayfa bağlantısı eklenmesi
- [x] Araç yedek parçası sektörüne uygun gerçek kategori verisinin (ve
      alt kategorilerinin) veri migration'ı ile eklenmesi
- [x] **Kategoriler** sayfası (üst seviye kategori kartları + alt kategoriler)
- [x] **Markalar** artık ayrı bir sayfa değil: navbar'da gerçek marka
      verisiyle dolu bir dropdown (masaüstünde hover-panel, mobilde
      `<details>` akordeon) — bir markaya tıklanınca o markanın tüm
      modellerine uyumlu ürünler listeleniyor, sayfa üstündeki model
      rozetleriyle (`?model=<slug>`) tek bir modele daraltılabiliyor
- [ ] Kategori sayfasından bir kategoriye tıklanınca marka/model'e göre
      filtrelenebilen ürün listesi (`schema.md`'deki Yol A gezinme akışının
      kalan kısmı — Yol B, yani marka-önce, artık yukarıdaki marka
      dropdown'ıyla karşılanmış durumda)
- [ ] Ürün detay sayfası
- [ ] Arama

---

Sonraki fazlar (arama, deploy yapılandırması vb.) Faz 3 tamamlandıktan
sonra ayrıca planlanacaktır.
