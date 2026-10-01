from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product

# Sadece müşteriye gösterilen açıklayıcı metinler çevrilebilir yapıldı.
# VehicleBrand/VehicleModel/PartBrand.ad ("Toyota", "Corolla", "Bosch") gibi
# özel isimler kasıtlı olarak dışarıda bırakıldı — bunlar her dilde aynı kalır.


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("ad", "aciklama")


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("ad", "aciklama")
