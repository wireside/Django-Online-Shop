from django.http import HttpResponse


def description(response):
    return HttpResponse("<body>О проекте</body>")
