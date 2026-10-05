from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline

from .models import HeroSlayt, IletisimMesaji, KurumsalSayfa, SayfaBasligi, SiteAyarlari


class TekKayitAdmin(TabbedTranslationAdmin):
    """Tek kayıtlı modeller: listeyi atlayıp doğrudan düzenleme sayfasını açar,
    yeni kayıt eklemeye ve silmeye izin vermez."""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        nesne = self.model.yukle()
        meta = self.model._meta
        return redirect(reverse(f"admin:{meta.app_label}_{meta.model_name}_change", args=[nesne.pk]))


@admin.register(SiteAyarlari)
class SiteAyarlariAdmin(TekKayitAdmin):
    fieldsets = (
        ("Genel", {
            "fields": ("site_adi", "logo", "logo_koyu_tema", "favicon", "meta_aciklama", "varsayilan_sayfa_gorseli", "footer_aciklama"),
            # Ana sayfa hero'su buradan değil Sayfa Başlıkları'ndan değişiyor; kolay bulunsun.
            "description": 'Ana sayfa ve diğer sayfaların başlık, yazı ve fotoğrafları: '
                           '<a href="../../../sayfabasligi/">Site İçeriği → Sayfa Başlıkları ve Fotoğrafları</a>',
        }),
        ("İletişim Bilgileri", {"fields": ("telefon", "whatsapp", "eposta", "adres", "calisma_saatleri", "harita_adresi")}),
        ("Sosyal Medya", {"fields": ("instagram", "facebook", "linkedin", "youtube")}),
    )


@admin.register(KurumsalSayfa)
class KurumsalSayfaAdmin(TekKayitAdmin):
    fieldsets = (
        ("Hakkımızda", {"fields": ("hakkimizda_baslik", "hakkimizda_metin", "hakkimizda_gorsel")}),
        ("Misyon", {"fields": ("misyon_baslik", "misyon_metin")}),
        ("Vizyon", {"fields": ("vizyon_baslik", "vizyon_metin")}),
        ("Neden Biz", {"fields": ("neden_biz_baslik", "neden_biz_maddeleri")}),
    )


class HeroSlaytInline(TranslationStackedInline):
    model = HeroSlayt
    extra = 0
    fields = ("gorsel", "ust_baslik", "baslik", "baslik_vurgu", "alt_baslik", "sira", "aktif")


@admin.register(SayfaBasligi)
class SayfaBasligiAdmin(TabbedTranslationAdmin):
    list_display = ("sayfa", "baslik", "gorsel_var_mi")
    list_display_links = ("sayfa", "baslik")

    def _anasayfa_mi(self, obj):
        return obj is not None and obj.sayfa == SayfaBasligi.Sayfa.ANASAYFA

    # Not: alanları get_fields ile gizlemek işe yaramıyor; modeltranslation formu
    # kendi kurarken get_fields'i yok sayıyor. get_exclude'u ise dikkate alıyor.
    def get_exclude(self, request, obj=None):
        # Ana sayfanın fotoğrafları tek görsel yerine slaytlarla yönetiliyor;
        # slayt süresi de sadece ana sayfada anlamlı.
        if self._anasayfa_mi(obj):
            return ("gorsel",)
        return ("slayt_suresi",)

    def get_inlines(self, request, obj):
        return [HeroSlaytInline] if self._anasayfa_mi(obj) else []

    # Sayfalar sabit; migration'la oluşturuluyor. Yeni ekleme/silme yok.
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return ("sayfa",)

    @admin.display(boolean=True, description="kendi fotoğrafı")
    def gorsel_var_mi(self, obj):
        if obj.sayfa == SayfaBasligi.Sayfa.ANASAYFA:
            return obj.slaytlar.filter(aktif=True).exists()
        return bool(obj.gorsel)


@admin.register(IletisimMesaji)
class IletisimMesajiAdmin(admin.ModelAdmin):
    list_display = ("ad_soyad", "konu", "eposta", "telefon", "gonderilme_tarihi", "okundu")
    list_filter = ("okundu", "gonderilme_tarihi")
    search_fields = ("ad_soyad", "eposta", "konu", "mesaj")
    readonly_fields = ("ad_soyad", "eposta", "telefon", "konu", "mesaj", "gonderilme_tarihi")
    actions = ["okundu_isaretle", "okunmadi_isaretle"]

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Mesaj açıldığında okundu say.
        IletisimMesaji.objects.filter(pk=object_id, okundu=False).update(okundu=True)
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.action(description="Seçilenleri okundu olarak işaretle")
    def okundu_isaretle(self, request, queryset):
        queryset.update(okundu=True)

    @admin.action(description="Seçilenleri okunmadı olarak işaretle")
    def okunmadi_isaretle(self, request, queryset):
        queryset.update(okundu=False)
