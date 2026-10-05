from modeltranslation.translator import TranslationOptions, register

from .models import HeroSlayt, KurumsalSayfa, SayfaBasligi, SiteAyarlari

# Her dilde ayrı girilebilen metinler. Bir dil boş bırakılırsa Türkçesi gösterilir.


@register(SiteAyarlari)
class SiteAyarlariTranslationOptions(TranslationOptions):
    fields = ("meta_aciklama", "footer_aciklama", "adres", "calisma_saatleri")


@register(SayfaBasligi)
class SayfaBasligiTranslationOptions(TranslationOptions):
    fields = ("ust_baslik", "baslik", "baslik_vurgu", "alt_baslik")


@register(KurumsalSayfa)
class KurumsalSayfaTranslationOptions(TranslationOptions):
    fields = (
        "hakkimizda_baslik", "hakkimizda_metin",
        "misyon_baslik", "misyon_metin",
        "vizyon_baslik", "vizyon_metin",
        "neden_biz_baslik", "neden_biz_maddeleri",
    )


@register(HeroSlayt)
class HeroSlaytTranslationOptions(TranslationOptions):
    fields = ("ust_baslik", "baslik", "baslik_vurgu", "alt_baslik")
