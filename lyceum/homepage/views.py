import http

import django.db.models
import django.http
import django.shortcuts
import django.urls

import catalog.models
import homepage.forms
import users.models

__all__ = ["coffee", "echo", "echo_submit", "home"]


def home(request):
    items = catalog.models.Item.objects.on_main()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, "homepage/main.html", context)


def echo(request):
    if request.method == "GET":
        echo_form = homepage.forms.EchoForm(request.POST or None)
        context = {"echo_form": echo_form}

        if echo_form.is_valid() and request.method == "POST":
            return django.http.HttpResponseBadRequest()
        else:
            return django.shortcuts.render(
                request=request,
                template_name="homepage/echo.html",
                context=context,
            )

    return django.http.HttpResponseNotAllowed(["POST"])


def echo_submit(request):
    if request.method == "POST":
        text = request.POST.get("text")
        return django.http.HttpResponse(
            text,
            content_type="text/plain",
            status=http.HTTPStatus.OK,
            charset="utf-16",
        )

    return django.http.HttpResponseNotAllowed(["GET"])


def coffee(response):
    if response.user.is_authenticated:
        user = users.models.Profile.objects.get(id=response.user.id)
        count = django.db.models.F(
            users.models.Profile.coffee_count.field.name,
        )
        user.coffee_count = count + 1
        user.save(
            update_fields=[
                users.models.Profile.coffee_count.field.name,
            ],
        )

    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )
