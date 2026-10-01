from .models import Category, VehicleBrand


def navbar_markalar(request):
    """Navbar'daki Markalar dropdown'ı (ve altındaki modeller) her sayfada
    erişilebilsin diye."""
    return {"NAVBAR_MARKALAR": VehicleBrand.objects.prefetch_related("modeller")}


def navbar_kategoriler(request):
    """Navbar'daki Kategoriler dropdown'ı için üst seviye kategoriler ve
    altlarındaki alt kategoriler (iç içe açılır menü için)."""
    return {
        "NAVBAR_KATEGORILER": Category.objects.filter(ust_kategori__isnull=True)
        .order_by("sira")
        .prefetch_related("alt_kategoriler")
    }
