from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def item_positive_converter(response, pk):
    return HttpResponse(f"<body>{pk}</body>")


def item_customer_converter(response, pk):
    return HttpResponse(f"<body>{pk}</body>")
