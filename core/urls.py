"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from catalog.views import index_view, iletisim_view, kategoriler_view, marka_urunleri_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # Turkish is the default and unprefixed ("/", "/iletisim/") — redirect anyone
    # who lands on "/tr/..." directly (bookmark, typed URL) to the real path
    # instead of a 404.
    path("tr/", RedirectView.as_view(url="/", permanent=False)),
    path("tr/iletisim/", RedirectView.as_view(url="/iletisim/", permanent=False)),
    path("tr/kategoriler/", RedirectView.as_view(url="/kategoriler/", permanent=False)),
    path(
        "tr/markalar/<slug:marka_slug>/",
        RedirectView.as_view(pattern_name="marka_urunleri", permanent=False),
    ),
]

# Default language (tr) keeps unprefixed URLs ("/", "/iletisim/"); the others
# get a language prefix ("/en/", "/fr/", "/es/", "/ar/") set by LocaleMiddleware.
urlpatterns += i18n_patterns(
    path("", index_view, name="index"),
    path("iletisim/", iletisim_view, name="iletisim"),
    path("kategoriler/", kategoriler_view, name="kategoriler"),
    # "Markalar" artık ayrı bir sayfa değil, navbar'daki dropdown'dan
    # doğrudan bir markaya tıklanınca açılan ürün listesi.
    path("markalar/<slug:marka_slug>/", marka_urunleri_view, name="marka_urunleri"),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
    # Cloudinary yapılandırılmamışken yerel MEDIA_ROOT'a düşen görselleri
    # (ör. admin'den yüklenen marka logosu) tarayıcıda görüntülemek için.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
