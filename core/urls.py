"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from catalog.views import (
    arama_urunler_view,
    arama_view,
    index_view,
    kategori_detay_view,
    kategoriler_view,
    marka_urunleri_view,
    urun_detay_view,
)
from icerik.views import iletisim_view, kurumsal_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # English is the default and unprefixed ("/", "/iletisim/") — redirect anyone
    # who lands on "/en/..." directly (bookmark, old link) to the real path
    # instead of a 404.
    path("en/", RedirectView.as_view(url="/", permanent=False)),
    path("en/iletisim/", RedirectView.as_view(url="/iletisim/", permanent=False)),
    path("en/kategoriler/", RedirectView.as_view(url="/kategoriler/", permanent=False)),
    path(
        "en/kategoriler/<slug:kategori_slug>/",
        RedirectView.as_view(pattern_name="kategori_detay", permanent=False),
    ),
    path("en/kurumsal/", RedirectView.as_view(url="/kurumsal/", permanent=False)),
    path(
        "en/markalar/<slug:marka_slug>/",
        RedirectView.as_view(pattern_name="marka_urunleri", permanent=False),
    ),
    path("en/arama/", RedirectView.as_view(pattern_name="arama", query_string=True, permanent=False)),
    path(
        "en/urun/<slug:urun_slug>/",
        RedirectView.as_view(pattern_name="urun_detay", permanent=False),
    ),
]

# Default language (en) keeps unprefixed URLs ("/", "/iletisim/"); the others
# get a language prefix ("/tr/", "/fr/", "/es/", "/ar/", "/ru/") set by LocaleMiddleware.
urlpatterns += i18n_patterns(
    path("", index_view, name="index"),
    path("iletisim/", iletisim_view, name="iletisim"),
    path("kurumsal/", kurumsal_view, name="kurumsal"),
    path("kategoriler/", kategoriler_view, name="kategoriler"),
    path("kategoriler/<slug:kategori_slug>/", kategori_detay_view, name="kategori_detay"),
    # "Markalar" artık ayrı bir sayfa değil, navbar'daki dropdown'dan
    # doğrudan bir markaya tıklanınca açılan ürün listesi.
    path("markalar/<slug:marka_slug>/", marka_urunleri_view, name="marka_urunleri"),
    # Ürün slug'ı tüm ürünler arasında benzersiz olduğu için marka/kategori
    # gibi değişebilen bilgileri URL'ye katmaya gerek yok — ürün başka bir
    # kategoriye taşınsa bile linki bozulmaz.
    path("urun/<slug:urun_slug>/", urun_detay_view, name="urun_detay"),
    path("arama/", arama_view, name="arama"),
    # Dil önekli olması (ör. /en/arama/urunler/) ürün adlarının o dilde
    # dönmesi için gerekli.
    path("arama/urunler/", arama_urunler_view, name="arama_urunler"),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
    # Cloudinary yapılandırılmamışken yerel MEDIA_ROOT'a düşen görselleri
    # (ör. admin'den yüklenen marka logosu) tarayıcıda görüntülemek için.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
