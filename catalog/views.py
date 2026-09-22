from django.shortcuts import render


def index_view(request):
    return render(request, "index.html")


def iletisim_view(request):
    return render(request, "iletisim.html")
