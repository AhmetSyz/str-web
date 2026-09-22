"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from catalog.views import index_view, iletisim_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # Turkish is the default and unprefixed ("/", "/iletisim/") — redirect anyone
    # who lands on "/tr/..." directly (bookmark, typed URL) to the real path
    # instead of a 404.
    path("tr/", RedirectView.as_view(url="/", permanent=False)),
    path("tr/iletisim/", RedirectView.as_view(url="/iletisim/", permanent=False)),
]

# Default language (tr) keeps unprefixed URLs ("/", "/iletisim/"); the others
# get a language prefix ("/en/", "/fr/", "/es/", "/ar/") set by LocaleMiddleware.
urlpatterns += i18n_patterns(
    path("", index_view, name="index"),
    path("iletisim/", iletisim_view, name="iletisim"),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
