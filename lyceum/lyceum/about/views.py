from django.shortcuts import render


def description(request):
    context = {}
    return render(request, "about/about.html", context)
