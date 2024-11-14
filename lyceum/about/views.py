from django.shortcuts import render

__all__ = ["description"]


def description(request):
    context = {}
    return render(request, "about/about.html", context)
