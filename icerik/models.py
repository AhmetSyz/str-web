from django.core.exceptions import ValidationError
from django.db import models


class TekKayit(models.Model):
    """Admin'de tek bir kaydı olan ayar modelleri için temel sınıf
    (Site Ayarları, Kurumsal Sayfa). Her zaman pk=1 kullanılır."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Silinirse site varsayılan değerlere döner ama kayıt kaybolmasın.
        pass

    @classmethod
    def yukle(cls):
        nesne, _ = cls.objects.get_or_create(pk=1)
        return nesne


def harita_adresi_dogrula(deger):
    # Sayfaya iframe olarak gömüldüğü için sadece Google Haritalar'ın
    # "Haritayı yerleştir" adresine izin veriliyor.
    if deger and not deger.startswith("https://www.google.com/maps/embed"):
        raise ValidationError(
            "Google Haritalar'da Paylaş → Haritayı yerleştir'deki kodun içindeki "
            "https://www.google.com/maps/embed?... ile başlayan adresi yapıştırın."
        )


class SiteAyarlari(TekKayit):
    site_adi = models.CharField("site adı", max_length=80, default="MARKA")
    logo = models.ImageField(
        "logo", upload_to="site/", blank=True,
        help_text="Açık temada (beyaz zemin) görünecek logo. Boşsa site adı yazı olarak gösterilir.",
    )
    logo_koyu_tema = models.ImageField(
        "logo (koyu tema)", upload_to="site/", blank=True,
        help_text="Koyu temada (lacivert zemin) görünecek, açık renkli logo. Boşsa yukarıdaki logo kullanılır.",
    )
    favicon = models.ImageField(
        "sekme ikonu (favicon)", upload_to="site/", blank=True,
        help_text="Tarayıcı sekmesinde görünen küçük kare ikon (PNG, en az 64×64).",
    )
    meta_aciklama = models.CharField(
        "site açıklaması (arama motorları)", max_length=200, blank=True,
        default="MARKA — kaliteli ürünler ve güvenilir hizmet.",
    )
    varsayilan_sayfa_gorseli = models.ImageField(
        "varsayılan üst fotoğraf", upload_to="site/", blank=True,
        help_text="Kendi fotoğrafı yüklenmemiş sayfaların (ana sayfa hariç) üstünde gösterilir. "
        "Ana sayfanın fotoğrafları: Site İçeriği → Sayfa Başlıkları ve Fotoğrafları → Ana Sayfa → Slaytlar.",
    )
    footer_aciklama = models.TextField(
        "footer açıklaması", blank=True,
        default="Kaliteli ürünler ve güvenilir hizmet için doğru adres.",
    )

    # İletişim
    telefon = models.CharField("telefon", max_length=40, blank=True, default="+90 (5xx) xxx xx xx")
    whatsapp = models.CharField(
        "WhatsApp numarası", max_length=20, blank=True,
        help_text="Ülke koduyla, boşluksuz: 905xxxxxxxxx. Boşsa WhatsApp butonu gösterilmez.",
    )
    eposta = models.EmailField("e-posta", blank=True, default="info@ornek.com")
    adres = models.TextField("adres", blank=True, default="Örnek Mahallesi, Sanayi Caddesi No: 1\nİstanbul, Türkiye")
    calisma_saatleri = models.CharField(
        "çalışma saatleri", max_length=120, blank=True, default="Pazartesi – Cumartesi, 09:00 – 18:00"
    )
    harita_adresi = models.URLField(
        "Google Haritalar yerleştirme adresi", max_length=1000, blank=True,
        validators=[harita_adresi_dogrula],
        help_text="Google Haritalar → Paylaş → Haritayı yerleştir → koddaki src=\"...\" içindeki adres.",
    )

    # Sosyal medya
    instagram = models.URLField("Instagram", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    youtube = models.URLField("YouTube", blank=True)

    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"

    def __str__(self):
        return "Site Ayarları"

    @property
    def whatsapp_linki(self):
        numara = "".join(c for c in self.whatsapp if c.isdigit())
        return f"https://wa.me/{numara}" if numara else ""

    @property
    def telefon_linki(self):
        return "tel:" + "".join(c for c in self.telefon if c.isdigit() or c == "+")


class SayfaBasligi(models.Model):
    """Her sayfanın üst (hero) bölümü: başlık, alt başlık ve arka plan görseli."""

    class Sayfa(models.TextChoices):
        ANASAYFA = "anasayfa", "Ana Sayfa"
        KATEGORILER = "kategoriler", "Kategoriler"
        ARAMA = "arama", "Parça Ara"
        KURUMSAL = "kurumsal", "Kurumsal"
        ILETISIM = "iletisim", "İletişim"

    sayfa = models.CharField("sayfa", max_length=20, choices=Sayfa.choices, unique=True)
    ust_baslik = models.CharField(
        "üst başlık", max_length=80, blank=True,
        help_text="Başlığın üstündeki küçük renkli yazı (ör. KALİTE VE GÜVEN).",
    )
    baslik = models.CharField("başlık", max_length=150)
    baslik_vurgu = models.CharField(
        "başlığın renkli kısmı", max_length=100, blank=True,
        help_text="Başlığın devamı olarak marka renginde gösterilir (ör. 'Tek Adreste').",
    )
    alt_baslik = models.TextField("alt başlık", blank=True)
    gorsel = models.ImageField(
        "üst fotoğraf", upload_to="sayfa_basliklari/", blank=True,
        help_text="Sayfanın en üstünde, başlığın arkasında gösterilir. Yatay, en az 1600 piksel "
        "genişliğinde bir fotoğraf önerilir. Boşsa Site Ayarları'ndaki varsayılan üst fotoğraf kullanılır.",
    )
    slayt_suresi = models.PositiveSmallIntegerField(
        "slayt süresi (saniye)", default=6,
        help_text="Sadece ana sayfa: her fotoğrafın ekranda kalma süresi.",
    )

    class Meta:
        verbose_name = "Sayfa Başlığı ve Fotoğrafı"
        verbose_name_plural = "Sayfa Başlıkları ve Fotoğrafları"
        ordering = ["id"]

    def __str__(self):
        return self.get_sayfa_display()

    @classmethod
    def getir(cls, sayfa):
        # Kayıt silinmişse sayfa çökmesin; boş bir başlıkla devam etsin.
        return cls.objects.filter(sayfa=sayfa).first() or cls(sayfa=sayfa, baslik="")


class HeroSlayt(models.Model):
    """Ana sayfa hero'sunda sırayla değişen fotoğraflar. Yazı alanları boşsa
    ana sayfanın kendi başlığı/alt başlığı gösterilir."""

    sayfa = models.ForeignKey(
        SayfaBasligi, on_delete=models.CASCADE, related_name="slaytlar", verbose_name="sayfa"
    )
    gorsel = models.ImageField(
        "fotoğraf", upload_to="hero/",
        help_text="Yatay, en az 1600 piksel genişliğinde bir fotoğraf önerilir.",
    )
    ust_baslik = models.CharField("üst başlık", max_length=80, blank=True)
    baslik = models.CharField("başlık", max_length=150, blank=True, help_text="Boşsa ana sayfa başlığı kullanılır.")
    baslik_vurgu = models.CharField("başlığın renkli kısmı", max_length=100, blank=True)
    alt_baslik = models.TextField("alt başlık", blank=True)
    sira = models.PositiveIntegerField("sıra", default=0)
    aktif = models.BooleanField("yayında", default=True)

    class Meta:
        verbose_name = "Slayt"
        verbose_name_plural = "Slaytlar (birden fazla eklenirse sırayla değişir)"
        ordering = ["sira", "id"]

    def __str__(self):
        return self.baslik or f"Slayt {self.sira}"


class KurumsalSayfa(TekKayit):
    hakkimizda_baslik = models.CharField("Hakkımızda başlığı", max_length=150, default="Hakkımızda")
    hakkimizda_metin = models.TextField("Hakkımızda metni", blank=True)
    hakkimizda_gorsel = models.ImageField("Hakkımızda görseli", upload_to="kurumsal/", blank=True)
    misyon_baslik = models.CharField("Misyon başlığı", max_length=150, default="Misyonumuz")
    misyon_metin = models.TextField("Misyon metni", blank=True)
    vizyon_baslik = models.CharField("Vizyon başlığı", max_length=150, default="Vizyonumuz")
    vizyon_metin = models.TextField("Vizyon metni", blank=True)
    neden_biz_baslik = models.CharField("Neden Biz başlığı", max_length=150, default="Neden Biz?")
    neden_biz_maddeleri = models.TextField(
        "Neden Biz maddeleri", blank=True,
        help_text="Her satıra bir madde yazın. İsterseniz 'Başlık: açıklama' şeklinde yazabilirsiniz.",
    )

    class Meta:
        verbose_name = "Kurumsal Sayfa"
        verbose_name_plural = "Kurumsal Sayfa"

    def __str__(self):
        return "Kurumsal Sayfa"

    @property
    def neden_biz_listesi(self):
        """Her satırı (başlık, açıklama) çiftine çevirir; ':' yoksa sadece başlık."""
        maddeler = []
        for satir in self.neden_biz_maddeleri.splitlines():
            satir = satir.strip()
            if not satir:
                continue
            baslik, ayrac, aciklama = satir.partition(":")
            maddeler.append((baslik.strip(), aciklama.strip()) if ayrac else (satir, ""))
        return maddeler


class IletisimMesaji(models.Model):
    ad_soyad = models.CharField("ad soyad", max_length=120)
    eposta = models.EmailField("e-posta")
    telefon = models.CharField("telefon", max_length=40, blank=True)
    konu = models.CharField("konu", max_length=200, blank=True)
    mesaj = models.TextField("mesaj")
    okundu = models.BooleanField("okundu", default=False)
    gonderilme_tarihi = models.DateTimeField("gönderilme tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Gelen Mesaj"
        verbose_name_plural = "Gelen Mesajlar"
        ordering = ["-gonderilme_tarihi"]

    def __str__(self):
        return f"{self.ad_soyad} – {self.konu or self.mesaj[:40]}"
