from django.db import migrations

# Sitede bu güne kadar şablonlara gömülü olan metinler, admin'den
# düzenlenebilsin diye veritabanına taşınıyor (5 dilde). Görseller boş
# başlar; boşken sitedeki mevcut yer tutucu görseller kullanılır.

DILLER = ("tr", "en", "fr", "es", "ar")

SAYFALAR = {
    "anasayfa": {
        "ust_baslik": ("Kalite ve Güven", "Quality and Trust", "Qualité et Confiance", "Calidad y Confianza", "الجودة والثقة"),
        "baslik": ("İhtiyacınız Olan Her Şey,", "Everything You Need,", "Tout ce dont vous avez besoin,", "Todo lo que necesita,", "كل ما تحتاجه،"),
        "baslik_vurgu": ("Tek Adreste", "In One Place", "en un seul endroit", "en un solo lugar", "في مكان واحد"),
        "alt_baslik": (
            "Geniş ürün yelpazemiz ve uzman ekibimizle yanınızdayız.",
            "We're here for you with our wide product range and expert team.",
            "Nous sommes à vos côtés avec notre large gamme de produits et notre équipe d'experts.",
            "Estamos a su lado con nuestra amplia gama de productos y nuestro equipo experto.",
            "نحن إلى جانبكم بتشكيلة واسعة من المنتجات وفريق من الخبراء.",
        ),
    },
    "kategoriler": {
        "baslik": ("Kategoriler", "Categories", "Catégories", "Categorías", "الفئات"),
        "alt_baslik": (
            "Aracınız için doğru parçayı bulmak üzere bir kategori seçin.",
            "Choose a category to find the right part for your vehicle.",
            "Choisissez une catégorie pour trouver la bonne pièce pour votre véhicule.",
            "Elija una categoría para encontrar la pieza correcta para su vehículo.",
            "اختر فئة للعثور على القطعة المناسبة لسيارتك.",
        ),
    },
    "arama": {
        "baslik": ("Parça Ara", "Find Parts", "Rechercher une pièce", "Buscar piezas", "البحث عن قطع"),
        "alt_baslik": (
            "Aracınızın markasını, modelini ve aradığınız parçanın kategorisini seçin.",
            "Select your vehicle's make and model and the category of the part you need.",
            "Sélectionnez la marque et le modèle de votre véhicule ainsi que la catégorie de la pièce recherchée.",
            "Seleccione la marca y el modelo de su vehículo y la categoría de la pieza que busca.",
            "اختر ماركة مركبتك وطرازها وفئة القطعة التي تبحث عنها.",
        ),
    },
    "kurumsal": {
        "baslik": ("Kurumsal", "About Us", "À propos", "Sobre nosotros", "من نحن"),
        "alt_baslik": (
            "Bizi daha yakından tanıyın.",
            "Get to know us better.",
            "Apprenez à mieux nous connaître.",
            "Conózcanos mejor.",
            "تعرّف علينا عن قرب.",
        ),
    },
    "iletisim": {
        "baslik": ("Bize Ulaşın", "Contact Us", "Contactez-nous", "Contáctenos", "تواصل معنا"),
        "alt_baslik": (
            "Sorularınız, talepleriniz ve iş birliği önerileriniz için formu doldurun, en kısa sürede size dönüş yapalım.",
            "Fill out the form for your questions, requests, and partnership proposals, and we'll get back to you as soon as possible.",
            "Remplissez le formulaire pour vos questions, demandes et propositions de partenariat, nous vous répondrons dans les plus brefs délais.",
            "Complete el formulario para sus preguntas, solicitudes y propuestas de colaboración; le responderemos lo antes posible.",
            "املأ النموذج لأسئلتك وطلباتك ومقترحات التعاون، وسنعاود التواصل معك في أقرب وقت ممكن.",
        ),
    },
}

SITE = {
    "meta_aciklama": (
        "MARKA — kaliteli ürünler ve güvenilir hizmet.",
        "MARKA — quality products and reliable service.",
        "MARKA — produits de qualité et service fiable.",
        "MARKA — productos de calidad y servicio confiable.",
        "MARKA — منتجات عالية الجودة وخدمة موثوقة.",
    ),
    "footer_aciklama": (
        "Kaliteli ürünler ve güvenilir hizmet için doğru adres.",
        "The right address for quality products and reliable service.",
        "La bonne adresse pour des produits de qualité et un service fiable.",
        "La dirección correcta para productos de calidad y un servicio confiable.",
        "العنوان الصحيح للمنتجات عالية الجودة والخدمة الموثوقة.",
    ),
    "adres": (
        "Örnek Mahallesi, Sanayi Caddesi No: 1\nİstanbul, Türkiye",
        "Örnek Neighborhood, Sanayi Street No: 1\nIstanbul, Turkey",
        "Örnek Mahallesi, Sanayi Caddesi n° 1\nIstanbul, Turquie",
        "Örnek Mahallesi, Sanayi Caddesi N.º 1\nEstambul, Turquía",
        "حي أورنك، شارع الصناعة رقم 1\nإسطنبول، تركيا",
    ),
    "calisma_saatleri": (
        "Pazartesi – Cumartesi, 09:00 – 18:00",
        "Monday – Saturday, 09:00 – 18:00",
        "Lundi – Samedi, 09h00 – 18h00",
        "Lunes – Sábado, 09:00 – 18:00",
        "الإثنين – السبت، 09:00 – 18:00",
    ),
}

KURUMSAL = {
    "hakkimizda_baslik": ("Hakkımızda", "About Us", "À propos de nous", "Sobre nosotros", "من نحن"),
    "misyon_baslik": ("Misyonumuz", "Our Mission", "Notre mission", "Nuestra misión", "مهمتنا"),
    "vizyon_baslik": ("Vizyonumuz", "Our Vision", "Notre vision", "Nuestra visión", "رؤيتنا"),
    "neden_biz_baslik": ("Neden Biz?", "Why Us?", "Pourquoi nous ?", "¿Por qué nosotros?", "لماذا نحن؟"),
}


def _doldur(nesne, alanlar):
    for alan, degerler in alanlar.items():
        for dil, deger in zip(DILLER, degerler):
            setattr(nesne, f"{alan}_{dil}", deger)
        # Asıl alan, varsayılan dilin (tr) değerini taşır.
        setattr(nesne, alan, degerler[0])


def ileri(apps, schema_editor):
    SayfaBasligi = apps.get_model("icerik", "SayfaBasligi")
    SiteAyarlari = apps.get_model("icerik", "SiteAyarlari")
    KurumsalSayfa = apps.get_model("icerik", "KurumsalSayfa")

    for sayfa, alanlar in SAYFALAR.items():
        nesne = SayfaBasligi.objects.filter(sayfa=sayfa).first() or SayfaBasligi(sayfa=sayfa)
        _doldur(nesne, alanlar)
        nesne.save()

    site = SiteAyarlari.objects.filter(pk=1).first() or SiteAyarlari(pk=1)
    _doldur(site, SITE)
    site.save()

    kurumsal = KurumsalSayfa.objects.filter(pk=1).first() or KurumsalSayfa(pk=1)
    _doldur(kurumsal, KURUMSAL)
    kurumsal.save()


def geri(apps, schema_editor):
    apps.get_model("icerik", "SayfaBasligi").objects.all().delete()
    apps.get_model("icerik", "SiteAyarlari").objects.all().delete()
    apps.get_model("icerik", "KurumsalSayfa").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("icerik", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(ileri, geri),
    ]
