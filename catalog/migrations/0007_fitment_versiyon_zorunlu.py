import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_uyumluluklari_versiyona_tasi"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="fitment",
            name="benzersiz_uyumluluk",
        ),
        migrations.RemoveField(
            model_name="fitment",
            name="arac_modeli",
        ),
        # 0006 tüm mevcut satırları doldurduğu için varsayılan gerekmiyor.
        migrations.AlterField(
            model_name="fitment",
            name="arac_versiyonu",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="uyumluluklar",
                to="catalog.vehicleversion",
                verbose_name="araç versiyonu",
            ),
        ),
        migrations.AddConstraint(
            model_name="fitment",
            constraint=models.UniqueConstraint(
                fields=("urun", "arac_versiyonu", "yil_baslangic", "yil_bitis"),
                name="benzersiz_uyumluluk",
            ),
        ),
    ]
