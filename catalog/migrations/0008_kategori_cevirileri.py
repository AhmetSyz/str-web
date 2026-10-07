from django.db import migrations

# 0003'te kategoriler sadece Türkçe adla oluşturulmuştu; diğer dillerde boş
# kaldıkları için modeltranslation Türkçeye düşüyordu (ör. "Conta Takımları"
# İngilizce sayfada da Türkçe görünüyordu). Slug'a göre eşleştirilir ve
# sadece BOŞ alanlar doldurulur: admin'den girilmiş bir çeviri ezilmez.

DILLER = ("en", "fr", "es", "ar")

CEVIRILER = {
    "motor-parcalari": ("Engine Parts", "Pièces moteur", "Piezas de motor", "قطع المحرك"),
    "motor-parcalari-motor-yagi-ve-filtreler": ("Engine Oil & Filters", "Huile moteur et filtres", "Aceite de motor y filtros", "زيت المحرك والفلاتر"),
    "motor-parcalari-kayis-kasnak-sistemi": ("Belt & Pulley System", "Courroies et poulies", "Correas y poleas", "نظام السيور والبكرات"),
    "motor-parcalari-conta-takimlari": ("Gasket Sets", "Jeux de joints", "Juegos de juntas", "أطقم الحشوات"),
    "fren-sistemi": ("Brake System", "Système de freinage", "Sistema de frenos", "نظام الفرامل"),
    "fren-sistemi-fren-balatasi": ("Brake Pads", "Plaquettes de frein", "Pastillas de freno", "فحمات الفرامل"),
    "fren-sistemi-fren-diski": ("Brake Discs", "Disques de frein", "Discos de freno", "أقراص الفرامل"),
    "fren-sistemi-fren-hidroligi": ("Brake Fluid", "Liquide de frein", "Líquido de frenos", "زيت الفرامل"),
    "suspansiyon-ve-direksiyon": ("Suspension & Steering", "Suspension et direction", "Suspensión y dirección", "التعليق والتوجيه"),
    "suspansiyon-ve-direksiyon-amortisor": ("Shock Absorbers", "Amortisseurs", "Amortiguadores", "ممتصات الصدمات"),
    "suspansiyon-ve-direksiyon-rotil-ve-rot-basi": ("Ball Joints & Tie Rod Ends", "Rotules et embouts de biellette", "Rótulas y terminales de dirección", "الوصلات الكروية وأطراف المقود"),
    "suspansiyon-ve-direksiyon-direksiyon-kremayeri": ("Steering Racks", "Crémaillères de direction", "Cremalleras de dirección", "جريدة التوجيه"),
    "sanziman-ve-debriyaj": ("Transmission & Clutch", "Transmission et embrayage", "Transmisión y embrague", "ناقل الحركة والقابض"),
    "elektrik-ve-aydinlatma": ("Electrical & Lighting", "Électricité et éclairage", "Electricidad e iluminación", "الكهرباء والإضاءة"),
    "elektrik-ve-aydinlatma-aku": ("Batteries", "Batteries", "Baterías", "البطاريات"),
    "elektrik-ve-aydinlatma-far-ve-sinyal-lambalari": ("Headlights & Signal Lamps", "Phares et clignotants", "Faros e intermitentes", "المصابيح الأمامية والإشارات"),
    "elektrik-ve-aydinlatma-mars-motoru-ve-alternator": ("Starters & Alternators", "Démarreurs et alternateurs", "Motores de arranque y alternadores", "محركات بدء التشغيل والدينامو"),
    "sogutma-sistemi": ("Cooling System", "Système de refroidissement", "Sistema de refrigeración", "نظام التبريد"),
    "sogutma-sistemi-radyator": ("Radiators", "Radiateurs", "Radiadores", "الرادياتير"),
    "sogutma-sistemi-termostat": ("Thermostats", "Thermostats", "Termostatos", "الثرموستات"),
    "yakit-sistemi": ("Fuel System", "Système d'alimentation", "Sistema de combustible", "نظام الوقود"),
    "yakit-sistemi-yakit-pompasi": ("Fuel Pumps", "Pompes à carburant", "Bombas de combustible", "مضخات الوقود"),
    "yakit-sistemi-enjektor": ("Injectors", "Injecteurs", "Inyectores", "البخاخات"),
    "filtreler": ("Filters", "Filtres", "Filtros", "الفلاتر"),
    "filtreler-hava-filtresi": ("Air Filters", "Filtres à air", "Filtros de aire", "فلاتر الهواء"),
    "filtreler-polen-filtresi": ("Cabin Filters", "Filtres d'habitacle", "Filtros de habitáculo", "فلاتر المقصورة"),
    "filtreler-yakit-filtresi": ("Fuel Filters", "Filtres à carburant", "Filtros de combustible", "فلاتر الوقود"),
    "egzoz-sistemi": ("Exhaust System", "Système d'échappement", "Sistema de escape", "نظام العادم"),
    "kaporta-ve-dis-aksam": ("Body & Exterior Parts", "Carrosserie et pièces extérieures", "Carrocería y piezas exteriores", "الهيكل والقطع الخارجية"),
    "ic-aksam-ve-doseme": ("Interior & Upholstery", "Intérieur et garnitures", "Interior y tapicería", "المقصورة الداخلية والتنجيد"),
    "klima-sistemi": ("Air Conditioning", "Climatisation", "Aire acondicionado", "نظام التكييف"),
}


def ileri(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    for kategori in Category.objects.filter(slug__in=CEVIRILER):
        degisen = []
        for dil, ad in zip(DILLER, CEVIRILER[kategori.slug]):
            alan = f"ad_{dil}"
            if not (getattr(kategori, alan) or "").strip():
                setattr(kategori, alan, ad)
                degisen.append(alan)
        if degisen:
            kategori.save(update_fields=degisen)


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_fitment_versiyon_zorunlu"),
    ]

    # Geri alınırken çeviriler silinmez (admin'den düzenlenmiş olabilirler).
    operations = [
        migrations.RunPython(ileri, migrations.RunPython.noop),
    ]
