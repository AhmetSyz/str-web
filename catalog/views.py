from django.shortcuts import get_object_or_404, render

from .models import Category, Product, VehicleBrand


def index_view(request):
    return render(request, "index.html")


def iletisim_view(request):
    return render(request, "iletisim.html")


def kategoriler_view(request):
    kategoriler = Category.objects.filter(ust_kategori__isnull=True).prefetch_related(
        "alt_kategoriler"
    )
    return render(request, "kategoriler.html", {"kategoriler": kategoriler})


def marka_urunleri_view(request, marka_slug):
    """Navbar'daki Markalar dropdown'ından bir markaya tıklandığında açılan
    sayfa: o markanın tüm modellerine uyumlu ürünler, modele göre
    filtrelenebilir (?model=<model-slug>)."""
    marka = get_object_or_404(VehicleBrand, slug=marka_slug)
    modeller = marka.modeller.all()

    secilen_model = None
    model_slug = request.GET.get("model")
    if model_slug:
        secilen_model = modeller.filter(slug=model_slug).first()

    urunler = Product.objects.filter(
        uyumluluklar__arac_modeli__marka=marka, aktif_mi=True
    ).distinct()
    if secilen_model:
        urunler = urunler.filter(uyumluluklar__arac_modeli=secilen_model)

    return render(
        request,
        "marka_urunleri.html",
        {
            "marka": marka,
            "modeller": modeller,
            "secilen_model": secilen_model,
            "urunler": urunler,
        },
    )
