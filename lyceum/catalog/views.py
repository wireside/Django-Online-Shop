import datetime
import random

import django.contrib
import django.db.models
import django.db.utils
import django.shortcuts
import django.urls
import django.utils.timezone

import catalog.models
import rating.forms
import rating.models

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
    ratings_stats = item.rating.aggregate(
        average=django.db.models.Avg("score"),
        count=django.db.models.Count("score"),
    )

    rating_form = rating.forms.RatingForm(request.POST or None)
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = rating.models.Rating.objects.get(
                item=item,
                user=request.user,
            )
            user_rating = user_rating.score
        except rating.models.Rating.DoesNotExist:
            user_rating = None

    if request.method == "POST" and rating_form.is_valid():
        try:
            new_rating = rating_form.save(commit=False)
            new_rating.user = request.user
            new_rating.item = item
            new_rating.save()
        except django.db.utils.IntegrityError:
            new_rating = rating.models.Rating.objects.get(
                user=request.user,
                item=item,
            )
            new_rating.score = rating_form.cleaned_data["score"]
            new_rating.save(
                update_fields=["score"],
            )

        return django.shortcuts.redirect(
            django.urls.reverse("catalog:item_detail", args=[pk]),
        )

    context = {
        "item": item,
        "rating_form": rating_form,
        "ratings_stats": ratings_stats,
        "user_rating": user_rating,
    }

    return django.shortcuts.render(request, "catalog/item.html", context)
