from http import HTTPStatus

from django.http import HttpResponse


# Create your views here.
def home(response):
    return HttpResponse("<body>Главная</body>")


def coffee(response):
    return HttpResponse(
        "Я чайник",
        status=HTTPStatus.IM_A_TEAPOT,
    )
