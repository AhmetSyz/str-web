from django.db import models
from django.utils.text import slugify

# Django'nun varsayılan slugify'ı Türkçe karakterleri (ı, ğ, ş, ö, ç, ü) doğrudan
# atıyor ("Direksiyon Sistemi" -> "dreksiyon-sistemi" gibi bozuk sonuçlar).
# Slug üretmeden önce bu karakterleri ASCII karşılıklarına çeviriyoruz.
_TR_CEVIRI_TABLOSU = str.maketrans("çÇğĞıİöÖşŞüÜ", "cCgGiIoOsSuU")


def turkce_slugify(value):
    return slugify(value.translate(_TR_CEVIRI_TABLOSU))


class Category(models.Model):
    ad = models.CharField("ad", max_length=100)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    ust_kategori = models.ForeignKey(
        "self",
        verbose_name="üst kategori",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="alt_kategoriler",
    )
    aciklama = models.TextField("açıklama", blank=True)
    # Her kategori kartının bir görseli olması gerektiği için zorunlu —
    # mevcut kayıtlar 0004 migration'ında bir placeholder ile dolduruldu,
    # admin'den gerçek fotoğrafla değiştirilmesi beklenir.
    gorsel = models.ImageField("görsel", upload_to="kategoriler/")
    sira = models.PositiveIntegerField("sıra", default=0)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ["sira", "ad"]

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = turkce_slugify(self.ad)
        super().save(*args, **kwargs)


class VehicleBrand(models.Model):
    ad = models.CharField("ad", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    logo = models.ImageField("logo", upload_to="arac_markalari/", blank=True, null=True)

    class Meta:
        verbose_name = "Araç Markası"
        verbose_name_plural = "Araç Markaları"
        ordering = ["ad"]

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = turkce_slugify(self.ad)
        super().save(*args, **kwargs)


class VehicleModel(models.Model):
    marka = models.ForeignKey(
        VehicleBrand, verbose_name="marka", on_delete=models.CASCADE, related_name="modeller"
    )
    ad = models.CharField("ad", max_length=100)
    slug = models.SlugField("slug", max_length=120, blank=True)
    uretim_baslangic_yili = models.PositiveIntegerField(
        "üretim başlangıç yılı", null=True, blank=True
    )
    uretim_bitis_yili = models.PositiveIntegerField("üretim bitiş yılı", null=True, blank=True)

    class Meta:
        verbose_name = "Araç Modeli"
        verbose_name_plural = "Araç Modelleri"
        ordering = ["marka__ad", "ad"]
        constraints = [
            models.UniqueConstraint(fields=["marka", "slug"], name="benzersiz_marka_slug"),
        ]

    def __str__(self):
        return f"{self.marka.ad} {self.ad}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = turkce_slugify(self.ad)
        super().save(*args, **kwargs)


class PartBrand(models.Model):
    ad = models.CharField("ad", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    logo = models.ImageField("logo", upload_to="parca_markalari/", blank=True, null=True)

    class Meta:
        verbose_name = "Parça Markası"
        verbose_name_plural = "Parça Markaları"
        ordering = ["ad"]

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = turkce_slugify(self.ad)
        super().save(*args, **kwargs)


class Product(models.Model):
    kategori = models.ForeignKey(
        Category,
        verbose_name="kategori",
        # Bir kategoriye bağlı ürün varken kategori yanlışlıkla silinip tüm
        # ürünlerin de gitmesini engellemek için PROTECT.
        on_delete=models.PROTECT,
        related_name="urunler",
    )
    parca_markasi = models.ForeignKey(
        PartBrand,
        verbose_name="parça markası",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="urunler",
    )
    ad = models.CharField("ad", max_length=200)
    slug = models.SlugField("slug", max_length=220, unique=True, blank=True)
    parca_numarasi = models.CharField(
        "parça numarası", max_length=100, unique=True, db_index=True
    )
    aciklama = models.TextField("açıklama", blank=True)
    fiyat = models.DecimalField("fiyat", max_digits=10, decimal_places=2)
    stok_adedi = models.PositiveIntegerField("stok adedi", default=0)
    ana_gorsel = models.ImageField("ana görsel", upload_to="urunler/", blank=True, null=True)
    aktif_mi = models.BooleanField("aktif mi", default=True)
    olusturulma_tarihi = models.DateTimeField("oluşturulma tarihi", auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField("güncellenme tarihi", auto_now=True)
    uyumlu_modeller = models.ManyToManyField(
        VehicleModel,
        through="Fitment",
        related_name="uyumlu_urunler",
        blank=True,
        verbose_name="uyumlu modeller",
    )

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ["-olusturulma_tarihi"]

    def __str__(self):
        return f"{self.ad} ({self.parca_numarasi})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = turkce_slugify(self.ad)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    urun = models.ForeignKey(
        Product, verbose_name="ürün", on_delete=models.CASCADE, related_name="gorseller"
    )
    gorsel = models.ImageField("görsel", upload_to="urun_gorselleri/")
    sira = models.PositiveIntegerField("sıra", default=0)

    class Meta:
        verbose_name = "Ürün Görseli"
        verbose_name_plural = "Ürün Görselleri"
        ordering = ["sira"]

    def __str__(self):
        return f"{self.urun.ad} - Görsel {self.sira}"


class Fitment(models.Model):
    urun = models.ForeignKey(
        Product, verbose_name="ürün", on_delete=models.CASCADE, related_name="uyumluluklar"
    )
    arac_modeli = models.ForeignKey(
        VehicleModel,
        verbose_name="araç modeli",
        on_delete=models.CASCADE,
        related_name="uyumluluklar",
    )
    yil_baslangic = models.PositiveIntegerField("yıl başlangıç", null=True, blank=True)
    yil_bitis = models.PositiveIntegerField("yıl bitiş", null=True, blank=True)

    class Meta:
        verbose_name = "Uyumluluk"
        verbose_name_plural = "Uyumluluklar"
        constraints = [
            models.UniqueConstraint(
                fields=["urun", "arac_modeli", "yil_baslangic", "yil_bitis"],
                name="benzersiz_uyumluluk",
            )
        ]

    def __str__(self):
        return f"{self.urun.ad} ↔ {self.arac_modeli}"
