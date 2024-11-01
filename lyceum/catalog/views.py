from django.shortcuts import render


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    context = {}
    return render(request, template, context)
