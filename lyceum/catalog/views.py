import datetime
import random

import django.db.models
import django.shortcuts

# from django.utils import timezone --> for UZE_TZ

import catalog.models


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
    items_ids = list(
        catalog.models.Item.objects.published()
        .filter(
            created__gte=datetime.datetime.now() - datetime.timedelta(days=7),
        )
        .values_list("pk", flat=True),
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
    items = (
        catalog.models.Item.objects.published()
        .filter(updated__week_day=6)
        .order_by(
            f"-{catalog.models.Item.updated.field.name}",
        )[:ITEMS_PER_PAGE]
    )

    context = {
        "items": items,
    }

    return django.shortcuts.render(request, "catalog/item_list.html", context)


def unverified(request):
    items = (
        catalog.models.Item.objects.published()
        .filter(
            created__gte=django.db.models.F(
                catalog.models.Item.updated.field.name,
            )
            - datetime.timedelta(seconds=1),
            created__lte=django.db.models.F(
                catalog.models.Item.updated.field.name,
            )
            + datetime.timedelta(seconds=1),
        )
        .order_by(
            "?",
        )
    )

    context = {
        "items": items,
    }

    return django.shortcuts.render(request, "catalog/item_list.html", context)


def item_detail(request, pk):
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.filter(is_published=True)
        .select_related(catalog.models.Item.category.field.name)
        .prefetch_related(
            django.db.models.Prefetch(
                catalog.models.Item.tags.field.name,
                catalog.models.Tag.objects.only(
                    catalog.models.Tag.name.field.name,
                ),
            ),
        )
        .only(
            catalog.models.Item.name.field.name,
            catalog.models.Item.text.field.name,
            f"{catalog.models.Item.category.field.name}"
            f"__{catalog.models.Category.name.field.name}",
            f"{catalog.models.Item.tags.field.name}"
            f"__{catalog.models.Tag.name.field.name}",
        ),
        pk=pk,
    )

    context = {
        "item": item,
    }

    return django.shortcuts.render(request, "catalog/item.html", context)
