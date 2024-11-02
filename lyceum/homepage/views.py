import http

import django.http
import django.shortcuts

import catalog.models


def home(request):
    items = catalog.models.Item.objects.filter(
        is_on_main=True,
        is_published=True,
    ).order_by("name")
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, "homepage/main.html", context)


def coffee(response):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )
