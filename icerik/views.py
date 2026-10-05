from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import IletisimFormu
from .models import KurumsalSayfa, SayfaBasligi


def iletisim_view(request):
    if request.method == "POST":
        form = IletisimFormu(request.POST)
        if form.is_valid():
            if not form.bot_mu():
                form.save()
            messages.success(request, _("Mesajınız alındı. En kısa sürede size dönüş yapacağız."))
            # Sayfa yenilenince formun tekrar gönderilmemesi için yönlendir.
            return redirect("iletisim")
    else:
        form = IletisimFormu()
    return render(
        request,
        "iletisim.html",
        {"form": form, "sayfa": SayfaBasligi.getir(SayfaBasligi.Sayfa.ILETISIM)},
    )


def kurumsal_view(request):
    return render(
        request,
        "kurumsal.html",
        {
            "sayfa": SayfaBasligi.getir(SayfaBasligi.Sayfa.KURUMSAL),
            "kurumsal": KurumsalSayfa.yukle(),
        },
    )
