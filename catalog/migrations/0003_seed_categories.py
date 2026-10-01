from django.db import migrations
from django.utils.text import slugify

# turkce_slugify'nin modeltranslation Category.save()'inden bagimsiz bir
# kopyasi: veri migration'lari canli model kodunu (catalog.models) degil,
# apps.get_model() ile o anki migration state'ini kullanir; bu yuzden
# ozel save() metodu burada calismaz, slug'i elle uretmemiz gerekiyor.
_TR_CEVIRI_TABLOSU = str.maketrans("çÇğĞıİöÖşŞüÜ", "cCgGiIoOsSuU")


def turkce_slugify(value):
    return slugify(value.translate(_TR_CEVIRI_TABLOSU))


# (üst kategori, [alt kategoriler]) — araç yedek parçası sektörüne uygun
# gerçek bir taksonomi. Açıklamalar ve diğer dillerin çevirileri admin
# panelinden ihtiyaç oldukça eklenebilir (bkz. schema.md "Çok Dilli İçerik").
KATEGORILER = [
    ("Motor Parçaları", [
        "Motor Yağı ve Filtreler",
        "Kayış-Kasnak Sistemi",
        "Conta Takımları",
    ]),
    ("Fren Sistemi", [
        "Fren Balatası",
        "Fren Diski",
        "Fren Hidroliği",
    ]),
    ("Süspansiyon ve Direksiyon", [
        "Amortisör",
        "Rotil ve Rot Başı",
        "Direksiyon Kremayeri",
    ]),
    ("Şanzıman ve Debriyaj", []),
    ("Elektrik ve Aydınlatma", [
        "Akü",
        "Far ve Sinyal Lambaları",
        "Marş Motoru ve Alternatör",
    ]),
    ("Soğutma Sistemi", [
        "Radyatör",
        "Termostat",
    ]),
    ("Yakıt Sistemi", [
        "Yakıt Pompası",
        "Enjektör",
    ]),
    ("Filtreler", [
        "Hava Filtresi",
        "Polen Filtresi",
        "Yakıt Filtresi",
    ]),
    ("Egzoz Sistemi", []),
    ("Kaporta ve Dış Aksam", []),
    ("İç Aksam ve Döşeme", []),
    ("Klima Sistemi", []),
]


def kategorileri_ekle(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")

    for sira, (ad, alt_kategoriler) in enumerate(KATEGORILER):
        ust = Category.objects.create(ad_tr=ad, slug=turkce_slugify(ad), sira=sira)
        for alt_sira, alt_ad in enumerate(alt_kategoriler):
            Category.objects.create(
                ad_tr=alt_ad,
                slug=f"{ust.slug}-{turkce_slugify(alt_ad)}",
                ust_kategori=ust,
                sira=alt_sira,
            )


def kategorileri_kaldir(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    isimler = [ad for ad, _ in KATEGORILER]
    Category.objects.filter(ad_tr__in=isimler).delete()  # CASCADE ile alt kategoriler de gider


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_category_aciklama_ar_category_aciklama_en_and_more"),
    ]

    operations = [
        migrations.RunPython(kategorileri_ekle, kategorileri_kaldir),
    ]
