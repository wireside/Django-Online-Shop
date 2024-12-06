import datetime
import random

import django.contrib
import django.db.models
import django.db.utils
import django.shortcuts
import django.urls
import django.utils.timezone
import django.views.generic

import cart.models
import catalog.models
import rating.forms
import rating.models

__all__ = []

ITEMS_PER_PAGE = 5


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    model = catalog.models.Item
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = catalog.models.Category.objects.published()
        return context


class NewItemsView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    model = catalog.models.Item

    def get_queryset(self):
        return catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_queryset = self.get_queryset()

        items_ids = base_queryset.filter(
            created__gte=django.utils.timezone.now()
            - datetime.timedelta(days=7),
        )

        items_ids = list(items_ids.values_list("pk", flat=True))

        try:
            selected = random.sample(items_ids, ITEMS_PER_PAGE)
        except ValueError:
            selected = items_ids

        context["items"] = base_queryset.filter(
            pk__in=selected,
        )

        return context


class FridayView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    model = catalog.models.Item

    def get_queryset(self):
        return catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = self.get_queryset()
        items = items.filter(updated__week_day=6)
        order_field = "-" + catalog.models.Item.updated.field.name
        items = (items.order_by(order_field))[:ITEMS_PER_PAGE]

        context["items"] = items

        return context


class UnverifiedView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    model = catalog.models.Item

    def get_queryset(self):
        return catalog.models.Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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
        context["items"] = items

        return context


class ItemDetailView(
    django.views.generic.DetailView,
    django.views.generic.FormView,
):
    template_name = "catalog/item.html"
    model = catalog.models.Item
    form_class = rating.forms.RatingForm
    context_object_name = "item"

    def get_queryset(self):
        return catalog.models.Item.objects.detail_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item = self.object

        ratings_stats = item.rating.aggregate(
            average=django.db.models.Avg("score"),
            count=django.db.models.Count("score"),
        )

        rating_form = self.form_class(self.request.POST or None)

        user_rating = None
        if self.request.user.is_authenticated:
            try:
                user_rating = rating.models.Rating.objects.get(
                    item=item,
                    user=self.request.user,
                ).score
            except rating.models.Rating.DoesNotExist:
                user_rating = None

        try:
            cart_item = cart.models.CartItem.objects.only("quantity").get(
                cart=self.request.user.cart,
                item=item,
            )
        except Exception:
            cart_item = None

        context.update(
            {
                "rating_form": rating_form,
                "ratings_stats": ratings_stats,
                "user_rating": user_rating,
                "cart_item": cart_item,
            },
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        item = self.object

        rating_form = self.form_class(request.POST)
        if rating_form.is_valid():
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
                new_rating.save(update_fields=["score"])

            return django.shortcuts.redirect(
                django.shortcuts.reverse(
                    "catalog:item_detail",
                    args=[item.pk],
                ),
            )

        return self.render_to_response(self.get_context_data(**kwargs))
