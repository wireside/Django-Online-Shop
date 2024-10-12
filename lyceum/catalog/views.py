from django.http import HttpResponse


def item_list(response):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(response, item_id):
    return HttpResponse("<body>Подробно элемент</body>")
