from django.shortcuts import render


def index(request):
    return render(request, "catalog/index.html")


def iletisim(request):
    return render(request, "catalog/iletisim.html")
