from django.db import migrations, models

VARSAYILAN_GORSEL = "kategoriler/varsayilan.jpg"


def gorseli_doldur(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.filter(gorsel="").update(gorsel=VARSAYILAN_GORSEL)
    Category.objects.filter(gorsel__isnull=True).update(gorsel=VARSAYILAN_GORSEL)


def gorseli_bosalt(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.filter(gorsel=VARSAYILAN_GORSEL).update(gorsel="")


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_seed_categories"),
    ]

    operations = [
        # 1) Önce boş/null olan tüm kategorilere placeholder ata — aksi
        #    halde 2. adımdaki NOT NULL/zorunlu alan değişikliği mevcut
        #    kayıtlarla çakışır.
        migrations.RunPython(gorseli_doldur, gorseli_bosalt),
        # 2) Alanı zorunlu hale getir.
        migrations.AlterField(
            model_name="category",
            name="gorsel",
            field=models.ImageField(upload_to="kategoriler/", verbose_name="görsel"),
        ),
    ]
