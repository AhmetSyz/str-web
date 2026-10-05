from django.db.models import F, Prefetch, Q, Value
from django.db.models.functions import Replace, Upper
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from icerik.models import HeroSlayt, SayfaBasligi

from .models import Category, Fitment, Product, VehicleBrand


def index_view(request):
    sayfa = SayfaBasligi.getir(SayfaBasligi.Sayfa.ANASAYFA)
    slaytlar = list(sayfa.slaytlar.filter(aktif=True)) if sayfa.pk else []
    if not slaytlar and sayfa.gorsel:
        # Eski tek "üst fotoğraf" alanına yüklenmiş görsel kaybolmasın: tek slayt
        # gibi göster (yazılar boş → ana sayfa başlığı kullanılır).
        slaytlar = [HeroSlayt(sayfa=sayfa, gorsel=sayfa.gorsel)]
    return render(request, "index.html", {"sayfa": sayfa, "slaytlar": slaytlar})


def kategoriler_view(request):
    kategoriler = Category.objects.filter(ust_kategori__isnull=True).prefetch_related(
        "alt_kategoriler"
    )
    return render(
        request,
        "kategoriler.html",
        {"kategoriler": kategoriler, "sayfa": SayfaBasligi.getir(SayfaBasligi.Sayfa.KATEGORILER)},
    )


def kategori_detay_view(request, kategori_slug):
    """Bir kategorinin ürünleri. Üst kategoriyse alt kategorilerindeki ürünler
    de listelenir; alt kategoriler üstte filtre etiketi olarak gösterilir."""
    kategori = get_object_or_404(
        Category.objects.select_related("ust_kategori"), slug=kategori_slug
    )
    # Etiketler: üst kategoride kendi alt kategorileri, alt kategoride kardeşleri.
    ust = kategori.ust_kategori or kategori
    alt_kategoriler = ust.alt_kategoriler.all()

    urunler = (
        Product.objects.filter(aktif_mi=True)
        .filter(Q(kategori=kategori) | Q(kategori__ust_kategori=kategori))
        .select_related("parca_markasi")
        .order_by("ad")
    )
    return render(
        request,
        "kategori_detay.html",
        {"kategori": kategori, "ust": ust, "alt_kategoriler": alt_kategoriler, "urunler": urunler},
    )


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
        uyumluluklar__arac_versiyonu__model__marka=marka, aktif_mi=True
    ).distinct()
    if secilen_model:
        urunler = urunler.filter(uyumluluklar__arac_versiyonu__model=secilen_model)

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


def urun_detay_view(request, urun_slug):
    urun = get_object_or_404(
        Product.objects.select_related(
            "kategori__ust_kategori", "parca_markasi"
        ).prefetch_related(
            "gorseller",
            "ozellikler",
            Prefetch(
                "uyumluluklar",
                queryset=Fitment.objects.select_related(
                    "arac_versiyonu__model__marka"
                ).order_by(
                    "arac_versiyonu__model__marka__ad",
                    "arac_versiyonu__model__ad",
                    "arac_versiyonu__ad",
                ),
            ),
        ),
        slug=urun_slug,
        aktif_mi=True,
    )
    uyumluluklar = list(urun.uyumluluklar.all())

    # Üstteki özet için: hangi marka/modellere uyduğu (tekrarsız, sıralı).
    uyumlu_modeller = list(
        dict.fromkeys(u.arac_versiyonu.model for u in uyumluluklar)
    )

    # Tüm uyumluluk satırlarını kapsayan genel yıl aralığı.
    baslangiclar = [
        u.yil_baslangic or u.arac_versiyonu.uretim_baslangic_yili for u in uyumluluklar
    ]
    bitisler = [u.yil_bitis or u.arac_versiyonu.uretim_bitis_yili for u in uyumluluklar]
    baslangiclar = [y for y in baslangiclar if y]
    bitisler = [y for y in bitisler if y]

    return render(
        request,
        "urun_detay.html",
        {
            "urun": urun,
            "uyumluluklar": uyumluluklar,
            "uyumlu_modeller": uyumlu_modeller,
            "yil_min": min(baslangiclar) if baslangiclar else None,
            "yil_max": max(bitisler) if bitisler else None,
        },
    )


# Parça kodları farklı yazılabiliyor ("BP-123", "bp 123", "BP.123");
# karşılaştırmadan önce bu ayırıcılar atılıp büyük harfe çevriliyor.
KOD_AYIRICILARI = ("-", " ", ".", "/", "_")


def _kodu_sadelestir(kod):
    kod = kod.upper()
    for ayirici in KOD_AYIRICILARI:
        kod = kod.replace(ayirici, "")
    return kod


def _sade_kod_ifadesi():
    """_kodu_sadelestir'in veritabanı tarafındaki karşılığı."""
    ifade = F("parca_numarasi")
    for ayirici in KOD_AYIRICILARI:
        ifade = Replace(ifade, Value(ayirici), Value(""))
    return Upper(ifade)


def _arama_filtreleri(params):
    """Ana sayfadaki arama çubuğunun (marka → model → kategori) ve parça kodu
    kutusunun (q) seçimlerine göre ürünleri filtreler. Hem sonuç sayfası hem
    de çubuktaki 'Ürün' listesini dolduran JSON endpoint'i aynı mantığı kullanır."""
    marka = params.get("marka", "")
    model = params.get("model", "")
    kategori = params.get("kategori", "")
    q = params.get("q", "").strip()

    urunler = Product.objects.filter(aktif_mi=True)
    if q:
        # Kodun bir kısmı da yetsin (ör. "123" → "BP-123"); kod bilmeyenler
        # ürün adıyla da arayabilsin.
        eslesme = Q(ad__icontains=q)
        sade = _kodu_sadelestir(q)
        if sade:
            urunler = urunler.annotate(sade_kod=_sade_kod_ifadesi())
            eslesme |= Q(sade_kod__contains=sade)
        urunler = urunler.filter(eslesme)
    if marka:
        urunler = urunler.filter(uyumluluklar__arac_versiyonu__model__marka__slug=marka)
    if model:
        # Model slug'ı sadece marka içinde benzersiz; marka seçilmediyse
        # aynı slug'lı farklı markaların modelleri de eşleşebilir.
        urunler = urunler.filter(uyumluluklar__arac_versiyonu__model__slug=model)
    if kategori:
        # Üst kategori seçildiyse alt kategorilerindeki ürünler de gelsin.
        urunler = urunler.filter(
            Q(kategori__slug=kategori) | Q(kategori__ust_kategori__slug=kategori)
        )
    return urunler.distinct()


def arama_view(request):
    urun_slug = request.GET.get("urun")
    if urun_slug:
        return redirect("urun_detay", urun_slug=urun_slug)

    # Kod birebir tek bir ürüne denk geliyorsa liste göstermeden ürüne git.
    q = request.GET.get("q", "").strip()
    if q and _kodu_sadelestir(q):
        tam_eslesen = list(
            Product.objects.filter(aktif_mi=True)
            .annotate(sade_kod=_sade_kod_ifadesi())
            .filter(sade_kod=_kodu_sadelestir(q))
            .values_list("slug", flat=True)[:2]
        )
        if len(tam_eslesen) == 1:
            return redirect("urun_detay", urun_slug=tam_eslesen[0])

    urunler = _arama_filtreleri(request.GET).order_by("ad")
    return render(
        request,
        "arama.html",
        {
            "sayfa": SayfaBasligi.getir(SayfaBasligi.Sayfa.ARAMA),
            "urunler": urunler,
            "secili": {k: request.GET.get(k, "").strip() for k in ("marka", "model", "kategori", "q")},
        },
    )


def arama_urunler_view(request):
    """Arama çubuğundaki 'Ürün' açılır listesini, önceki seçimlere uyan
    ürünlerle doldurmak için."""
    urunler = _arama_filtreleri(request.GET).order_by("ad").values(
        "slug", "ad", "parca_numarasi"
    )[:200]
    return JsonResponse({"urunler": list(urunler)})
