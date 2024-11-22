import http

import django.contrib.auth.mixins
import django.db.models
import django.http
import django.shortcuts
import django.urls
import django.views.generic

import catalog.models
import homepage.forms

__all__ = []


class HomeView(django.views.generic.ListView):
    template_name = "homepage/main.html"
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.on_main()


class EchoView(django.views.generic.FormView):
    template_name = "homepage/echo.html"
    context_object_name = "echo_form"
    form_class = homepage.forms.EchoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["echo_form"] = self.form_class(self.request.POST or None)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return django.shortcuts.render(
            request=request,
            template_name=self.template_name,
            context=context,
        )

    def post(self, request, *args, **kwargs):
        return django.http.HttpResponseNotAllowed(["GET"])


class EchoSubmitView(django.views.generic.FormView):
    template_name = "homepage/echo.html"

    def get(self, request, *args, **kwargs):
        return django.http.HttpResponseNotAllowed(["POST"])

    def post(self, request, *args, **kwargs):
        text = request.POST.get("text")
        return django.http.HttpResponse(
            text,
            content_type="text/plain; charset=utf-8",
            status=http.HTTPStatus.OK,
        )


class CoffeeView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.profile.coffee_count += 1
            request.user.profile.save()

        return django.http.HttpResponse(
            "Я чайник",
            status=http.HTTPStatus.IM_A_TEAPOT,
        )
