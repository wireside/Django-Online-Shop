import django.views.generic

__all__ = []


class DescriptionView(django.views.generic.TemplateView):
    template_name = "about/about.html"
