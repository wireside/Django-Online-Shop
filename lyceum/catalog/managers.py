import django.db.models

import catalog.models

__all__ = ["CategoryManager", "ItemManager"]


class ItemManager(django.db.models.Manager):
    def on_main(self):
        return (
            self.published()
            .filter(is_on_main=True)
            .order_by(
                catalog.models.Item.name.field.name,
            )
        )

    def published(self):
        queryset = self.get_queryset()

        filters = {
            "is_published": True,
            "category__is_published": True,
        }

        select_related_fields = [
            catalog.models.Item.category.field.name,
            catalog.models.Item.main_image.related.name,
        ]

        tag_name_field = catalog.models.Tag.name.field.name
        tags_prefetch = django.db.models.Prefetch(
            catalog.models.Item.tags.field.name,
            queryset=catalog.models.Tag.objects.only(tag_name_field),
        )

        item_name_field = catalog.models.Item.name.field.name
        item_text_field = catalog.models.Item.text.field.name
        main_image_field = catalog.models.Item.main_image.related.name
        category_name_field = [
            catalog.models.Item.category.field.name,
            catalog.models.Category.name.field.name,
        ]
        category_name_field = "__".join(category_name_field)
        tag_field = [
            catalog.models.Item.tags.field.name,
            catalog.models.Tag.name.field.name,
        ]
        tag_field = "__".join(tag_field)
        only_fields = [
            item_name_field,
            item_text_field,
            main_image_field,
            category_name_field,
            tag_field,
        ]

        order_by_fields = [
            category_name_field,
            item_name_field,
        ]

        queryset = queryset.filter(**filters)

        queryset = queryset.select_related(*select_related_fields)

        queryset = queryset.prefetch_related(tags_prefetch)

        queryset = queryset.only(*only_fields)

        queryset = queryset.order_by(*order_by_fields)

        return queryset

    def detail_published(self):
        queryset = self.get_queryset()

        filters = {
            "is_published": True,
            "category__is_published": True,
        }

        select_related_fields = [
            catalog.models.Item.category.field.name,
        ]

        tags_prefetch = django.db.models.Prefetch(
            catalog.models.Item.tags.field.name,
            queryset=catalog.models.Tag.objects.only(
                catalog.models.Tag.name.field.name,
            ),
        )

        item_name_field = catalog.models.Item.name.field.name
        item_text_field = catalog.models.Item.text.field.name
        main_image_field = catalog.models.Item.main_image.related.name
        category_name_field = [
            catalog.models.Item.category.field.name,
            catalog.models.Category.name.field.name,
        ]
        category_name_field = "__".join(category_name_field)
        tag_field = [
            catalog.models.Item.tags.field.name,
            catalog.models.Tag.name.field.name,
        ]
        tag_field = "__".join(tag_field)
        only_fields = [
            item_name_field,
            item_text_field,
            main_image_field,
            category_name_field,
            tag_field,
        ]

        order_by_fields = [
            category_name_field,
            item_name_field,
        ]

        queryset = queryset.filter(**filters)

        queryset = queryset.select_related(*select_related_fields)

        queryset = queryset.prefetch_related(tags_prefetch)

        queryset = queryset.only(*only_fields)

        queryset = queryset.order_by(*order_by_fields)

        return queryset


class CategoryManager(django.db.models.Manager):
    def published(self):
        queryset = self.get_queryset()

        field_name = catalog.models.Category.name.field.name
        order_field = f"-{field_name}"

        queryset = queryset.filter(is_published=True)

        queryset = queryset.exclude(items__exact=None)

        queryset = queryset.only(field_name)

        queryset = queryset.order_by(order_field)

        return queryset
