from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("iletisim/", views.iletisim_view, name="iletisim"),
]
