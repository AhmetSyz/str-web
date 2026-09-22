"""
URL configuration for core project.
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from catalog.views import index_view, iletisim_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index_view, name="index"),
    path("iletisim/", iletisim_view, name="iletisim"),
]

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
