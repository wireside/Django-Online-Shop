import datetime
import random

import django.db.models
import django.shortcuts
import django.utils.timezone

import catalog.models

__all__ = ["friday", "item_detail", "item_list", "new", "unverified"]


ITEMS_PER_PAGE = 5


def item_list(request):
    items = catalog.models.Item.objects.published()

    categories = catalog.models.Category.objects.published()

    context = {
        "items": items,
        "categories": categories,
    }

    return django.shortcuts.render(request, "catalog/item_list.html", context)


def new(request):
    items_ids = catalog.models.Item.objects.published()

    items_ids = items_ids.filter(
        created__gte=django.utils.timezone.now() - datetime.timedelta(days=7),
    )
    items_ids = list(
        items_ids.values_list("pk", flat=True),
    )

    try:
        selected = random.sample(items_ids, ITEMS_PER_PAGE)
    except ValueError:
        selected = items_ids

    items = catalog.models.Item.objects.published().filter(pk__in=selected)

    context = {
        "items": items,
    }

    return django.shortcuts.render(request, "catalog/item_list.html", context)


def friday(request):
    items = catalog.models.Item.objects.published()
    items = items.filter(updated__week_day=6)
    order_field = "-" + catalog.models.Item.updated.field.name
    items = (items.order_by(order_field))[:ITEMS_PER_PAGE]

    context = {
        "items": items,
    }

    return django.shortcuts.render(request, "catalog/item_list.html", context)


def unverified(request):
    items = catalog.models.Item.objects.published()
    items = items.filter(
        created__gte=django.db.models.F(
            catalog.models.Item.updated.field.name,
        )
        - datetime.timedelta(seconds=1),
        created__lte=django.db.models.F(
            catalog.models.Item.updated.field.name,
        )
        + datetime.timedelta(seconds=1),
    )
    items = items.order_by(
        "?",
    )

    context = {
        "items": items,
    }

    return django.shortcuts.render(request, "catalog/item_list.html", context)


def item_detail(request, pk):
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.detail_published(),
        pk=pk,
    )

    context = {
        "item": item,
    }

    return django.shortcuts.render(request, "catalog/item.html", context)
