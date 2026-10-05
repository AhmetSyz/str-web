from django import forms
from django.utils.translation import gettext_lazy as _

from .models import IletisimMesaji


class IletisimFormu(forms.ModelForm):
    # Botlar genelde tüm alanları doldurur; gerçek kullanıcılar bu gizli alanı
    # görmez. Dolu gelirse mesaj sessizce yok sayılır.
    web_sitesi = forms.CharField(required=False)

    class Meta:
        model = IletisimMesaji
        fields = ["ad_soyad", "eposta", "telefon", "konu", "mesaj"]
        labels = {
            "ad_soyad": _("Ad Soyad"),
            "eposta": _("E-posta"),
            "telefon": _("Telefon"),
            "konu": _("Konu"),
            "mesaj": _("Mesajınız"),
        }

    def bot_mu(self):
        return bool(self.cleaned_data.get("web_sitesi"))
