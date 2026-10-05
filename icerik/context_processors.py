from .models import SiteAyarlari


def site_ayarlari(request):
    """Logo, site adı, iletişim bilgileri gibi her sayfada (navbar/footer)
    kullanılan ayarlar."""
    return {"SITE": SiteAyarlari.yukle()}
