from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product, ProductFeature

# Sadece müşteriye gösterilen açıklayıcı metinler çevrilebilir yapıldı.
# VehicleBrand/VehicleModel/PartBrand.ad ("Toyota", "Corolla", "Bosch") gibi
# özel isimler kasıtlı olarak dışarıda bırakıldı — bunlar her dilde aynı kalır.


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("ad", "aciklama")


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("ad", "aciklama")


@register(ProductFeature)
class ProductFeatureTranslationOptions(TranslationOptions):
    # "Renk: Siyah" gibi değerler de dile göre değişebildiği için ikisi de.
    fields = ("ad", "deger")
