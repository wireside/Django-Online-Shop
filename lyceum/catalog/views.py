import django.shortcuts

import catalog.models


def item_list(request):
    items = catalog.models.Item.objects.published()
    categories = (
        catalog.models.Category.objects.all().only("name").order_by("-name")
    )
    context = {
        "items": items,
        "categories": categories,
    }
    return django.shortcuts.render(request, "catalog/item_list.html", context)


def item_detail(request, pk):
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.filter(is_published=True),
        pk=pk,
    )
    context = {
        "item": item,
    }
    return django.shortcuts.render(request, "catalog/item.html", context)
