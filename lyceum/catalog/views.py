from django.http import HttpResponse


def item_list(response):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(response, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def item_positive_converter(response, pk):
    return HttpResponse(f"<body>{pk}</body>")


def item_customer_converter(response, pk):
    return HttpResponse(f"<body>{pk}</body>")
