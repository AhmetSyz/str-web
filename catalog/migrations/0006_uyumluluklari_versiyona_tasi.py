from django.db import migrations

# Uyumluluk artık modele değil versiyona bağlanıyor. Mevcut kayıtlar
# kaybolmasın diye, uyumluluğu olan her model için "Standart" adlı bir
# versiyon oluşturulup kayıtlar ona taşınıyor. Admin'den bu versiyonun
# adı, motor hacmi ve kasa tipi gerçek değerlerle düzeltilmeli.
VARSAYILAN_VERSIYON_ADI = "Standart"


def ileri(apps, schema_editor):
    Fitment = apps.get_model("catalog", "Fitment")
    VehicleVersion = apps.get_model("catalog", "VehicleVersion")

    for uyumluluk in Fitment.objects.select_related("arac_modeli"):
        model = uyumluluk.arac_modeli
        versiyon, _ = VehicleVersion.objects.get_or_create(
            model=model,
            ad=VARSAYILAN_VERSIYON_ADI,
            defaults={
                "uretim_baslangic_yili": model.uretim_baslangic_yili,
                "uretim_bitis_yili": model.uretim_bitis_yili,
            },
        )
        uyumluluk.arac_versiyonu = versiyon
        uyumluluk.save(update_fields=["arac_versiyonu"])


def geri(apps, schema_editor):
    Fitment = apps.get_model("catalog", "Fitment")
    for uyumluluk in Fitment.objects.select_related("arac_versiyonu"):
        uyumluluk.arac_modeli_id = uyumluluk.arac_versiyonu.model_id
        uyumluluk.save(update_fields=["arac_modeli"])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_arac_versiyonu_urun_ozellikleri"),
    ]

    operations = [
        migrations.RunPython(ileri, geri),
    ]
