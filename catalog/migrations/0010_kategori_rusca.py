from django.db import migrations

# 0008'deki gibi: kategorilerin Rusça adları, slug'a göre. Sadece BOŞ
# alanlar doldurulur; admin'den girilmiş bir çeviri ezilmez.

CEVIRILER = {
    "motor-parcalari": "Детали двигателя",
    "motor-parcalari-motor-yagi-ve-filtreler": "Моторное масло и фильтры",
    "motor-parcalari-kayis-kasnak-sistemi": "Ремни и шкивы",
    "motor-parcalari-conta-takimlari": "Комплекты прокладок",
    "fren-sistemi": "Тормозная система",
    "fren-sistemi-fren-balatasi": "Тормозные колодки",
    "fren-sistemi-fren-diski": "Тормозные диски",
    "fren-sistemi-fren-hidroligi": "Тормозная жидкость",
    "suspansiyon-ve-direksiyon": "Подвеска и рулевое управление",
    "suspansiyon-ve-direksiyon-amortisor": "Амортизаторы",
    "suspansiyon-ve-direksiyon-rotil-ve-rot-basi": "Шаровые опоры и рулевые наконечники",
    "suspansiyon-ve-direksiyon-direksiyon-kremayeri": "Рулевые рейки",
    "sanziman-ve-debriyaj": "Трансмиссия и сцепление",
    "elektrik-ve-aydinlatma": "Электрика и освещение",
    "elektrik-ve-aydinlatma-aku": "Аккумуляторы",
    "elektrik-ve-aydinlatma-far-ve-sinyal-lambalari": "Фары и указатели поворота",
    "elektrik-ve-aydinlatma-mars-motoru-ve-alternator": "Стартеры и генераторы",
    "sogutma-sistemi": "Система охлаждения",
    "sogutma-sistemi-radyator": "Радиаторы",
    "sogutma-sistemi-termostat": "Термостаты",
    "yakit-sistemi": "Топливная система",
    "yakit-sistemi-yakit-pompasi": "Топливные насосы",
    "yakit-sistemi-enjektor": "Форсунки",
    "filtreler": "Фильтры",
    "filtreler-hava-filtresi": "Воздушные фильтры",
    "filtreler-polen-filtresi": "Салонные фильтры",
    "filtreler-yakit-filtresi": "Топливные фильтры",
    "egzoz-sistemi": "Выхлопная система",
    "kaporta-ve-dis-aksam": "Кузов и внешние детали",
    "ic-aksam-ve-doseme": "Салон и обивка",
    "klima-sistemi": "Кондиционер",
}


def ileri(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    for kategori in Category.objects.filter(slug__in=CEVIRILER):
        if not (kategori.ad_ru or "").strip():
            kategori.ad_ru = CEVIRILER[kategori.slug]
            kategori.save(update_fields=["ad_ru"])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0009_rusca_alanlar"),
    ]

    operations = [
        migrations.RunPython(ileri, migrations.RunPython.noop),
    ]
