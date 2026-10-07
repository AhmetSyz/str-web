from django.db import migrations

# 0002'de eklenen başlangıç metinlerinin Rusçası. Bir alanın Rusçası sadece
# boşsa VE Türkçesi hâlâ başlangıçtaki metinse doldurulur: admin'den Türkçesi
# değiştirilmiş bir metne eski metnin çevirisi yazılmasın.

SAYFALAR = {
    "anasayfa": {
        "ust_baslik": ("Kalite ve Güven", "Качество и надёжность"),
        "baslik": ("İhtiyacınız Olan Her Şey,", "Всё, что вам нужно,"),
        "baslik_vurgu": ("Tek Adreste", "в одном месте"),
        "alt_baslik": (
            "Geniş ürün yelpazemiz ve uzman ekibimizle yanınızdayız.",
            "Мы рядом с вами благодаря широкому ассортименту и команде экспертов.",
        ),
    },
    "kategoriler": {
        "baslik": ("Kategoriler", "Категории"),
        "alt_baslik": (
            "Aracınız için doğru parçayı bulmak üzere bir kategori seçin.",
            "Выберите категорию, чтобы найти подходящую деталь для вашего автомобиля.",
        ),
    },
    "arama": {
        "baslik": ("Parça Ara", "Поиск запчастей"),
        "alt_baslik": (
            "Aracınızın markasını, modelini ve aradığınız parçanın kategorisini seçin.",
            "Выберите марку и модель автомобиля, а также категорию нужной детали.",
        ),
    },
    "kurumsal": {
        "baslik": ("Kurumsal", "О компании"),
        "alt_baslik": ("Bizi daha yakından tanıyın.", "Узнайте нас поближе."),
    },
    "iletisim": {
        "baslik": ("Bize Ulaşın", "Свяжитесь с нами"),
        "alt_baslik": (
            "Sorularınız, talepleriniz ve iş birliği önerileriniz için formu doldurun, en kısa sürede size dönüş yapalım.",
            "Заполните форму, чтобы задать вопрос, оставить заявку или предложить сотрудничество, и мы свяжемся с вами в ближайшее время.",
        ),
    },
}

SITE = {
    "meta_aciklama": (
        "MARKA — kaliteli ürünler ve güvenilir hizmet.",
        "MARKA — качественная продукция и надёжный сервис.",
    ),
    "footer_aciklama": (
        "Kaliteli ürünler ve güvenilir hizmet için doğru adres.",
        "Правильный адрес для качественной продукции и надёжного сервиса.",
    ),
    "adres": (
        "Örnek Mahallesi, Sanayi Caddesi No: 1\nİstanbul, Türkiye",
        "Örnek Mahallesi, Sanayi Caddesi, д. 1\nСтамбул, Турция",
    ),
    "calisma_saatleri": (
        "Pazartesi – Cumartesi, 09:00 – 18:00",
        "Понедельник – суббота, 09:00 – 18:00",
    ),
}

KURUMSAL = {
    "hakkimizda_baslik": ("Hakkımızda", "О нас"),
    "misyon_baslik": ("Misyonumuz", "Наша миссия"),
    "vizyon_baslik": ("Vizyonumuz", "Наше видение"),
    "neden_biz_baslik": ("Neden Biz?", "Почему мы?"),
}


def _sade(metin):
    return (metin or "").replace("\r\n", "\n").strip()


def _doldur(nesne, alanlar):
    degisen = []
    for alan, (tr, ru) in alanlar.items():
        mevcut_ru = _sade(getattr(nesne, f"{alan}_ru"))
        # SiteAyarlari alanlarının varsayılanı Türkçe metin; 0005'te eklenen
        # _ru kolonları mevcut satırda bu Türkçe varsayılanla doldu. Onu da
        # boş say.
        if mevcut_ru and mevcut_ru != tr:
            continue
        if _sade(getattr(nesne, f"{alan}_tr")) == tr:
            yeni = ru
        else:
            # Türkçesi admin'den değiştirilmiş: Rusçayı boşalt ki güncel
            # Türkçe metne düşsün, eski varsayılan metin görünmesin.
            yeni = None
        if getattr(nesne, f"{alan}_ru") != yeni:
            setattr(nesne, f"{alan}_ru", yeni)
            degisen.append(f"{alan}_ru")
    if degisen:
        nesne.save(update_fields=degisen)


def ileri(apps, schema_editor):
    SayfaBasligi = apps.get_model("icerik", "SayfaBasligi")
    for nesne in SayfaBasligi.objects.filter(sayfa__in=SAYFALAR):
        _doldur(nesne, SAYFALAR[nesne.sayfa])
    for nesne in apps.get_model("icerik", "SiteAyarlari").objects.filter(pk=1):
        _doldur(nesne, SITE)
    for nesne in apps.get_model("icerik", "KurumsalSayfa").objects.filter(pk=1):
        _doldur(nesne, KURUMSAL)


class Migration(migrations.Migration):

    dependencies = [
        ("icerik", "0005_rusca_alanlar"),
    ]

    operations = [
        migrations.RunPython(ileri, migrations.RunPython.noop),
    ]
