from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline

from .models import (
    Category,
    Fitment,
    PartBrand,
    Product,
    ProductFeature,
    ProductImage,
    VehicleBrand,
    VehicleModel,
    VehicleVersion,
)


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ("ad", "ust_kategori", "sira")
    list_filter = ("ust_kategori",)
    search_fields = ("ad",)
    prepopulated_fields = {"slug": ("ad",)}


class VehicleModelInline(admin.TabularInline):
    model = VehicleModel
    extra = 1
    prepopulated_fields = {"slug": ("ad",)}


@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = ("ad",)
    search_fields = ("ad",)
    prepopulated_fields = {"slug": ("ad",)}
    inlines = [VehicleModelInline]


class VehicleVersionInline(admin.TabularInline):
    model = VehicleVersion
    extra = 1


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ("ad", "marka", "uretim_baslangic_yili", "uretim_bitis_yili")
    list_filter = ("marka",)
    search_fields = ("ad", "marka__ad")
    prepopulated_fields = {"slug": ("ad",)}
    inlines = [VehicleVersionInline]


@admin.register(VehicleVersion)
class VehicleVersionAdmin(admin.ModelAdmin):
    list_display = ("ad", "model", "motor_hacmi", "kasa_tipi", "uretim_baslangic_yili", "uretim_bitis_yili")
    list_filter = ("model__marka", "kasa_tipi")
    # Ürün admin'indeki uyumluluk satırlarında autocomplete için gerekli.
    search_fields = ("ad", "model__ad", "model__marka__ad")
    list_select_related = ("model__marka",)


@admin.register(PartBrand)
class PartBrandAdmin(admin.ModelAdmin):
    list_display = ("ad",)
    search_fields = ("ad",)
    prepopulated_fields = {"slug": ("ad",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductFeatureInline(TranslationTabularInline):
    model = ProductFeature
    extra = 1


class FitmentInline(admin.TabularInline):
    model = Fitment
    extra = 1
    autocomplete_fields = ["arac_versiyonu"]


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_display = (
        "ad",
        "parca_numarasi",
        "kategori",
        "parca_markasi",
        "stok_adedi",
        "aktif_mi",
    )
    list_filter = ("kategori", "parca_markasi", "aktif_mi")
    search_fields = ("ad", "parca_numarasi")
    prepopulated_fields = {"slug": ("ad",)}
    inlines = [ProductImageInline, ProductFeatureInline, FitmentInline]
