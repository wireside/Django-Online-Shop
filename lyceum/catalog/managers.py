import django.db.models

import catalog.models


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
        return (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .select_related(
                catalog.models.Item.category.field.name,
                catalog.models.Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.tags.field.name,
                    queryset=catalog.models.Tag.objects.only(
                        catalog.models.Tag.name.field.name,
                    ),
                ),
            )
            .only(
                catalog.models.Item.name.field.name,
                catalog.models.Item.text.field.name,
                catalog.models.Item.main_image.related.name,
                f"{catalog.models.Item.category.field.name}"
                f"__{catalog.models.Category.name.field.name}",
                f"{catalog.models.Item.tags.field.name}"
                f"__{catalog.models.Tag.name.field.name}",
            )
            .order_by(
                f"{catalog.models.Item.category.field.name}"
                f"__{catalog.models.Category.name.field.name}",
                catalog.models.Item.name.field.name,
            )
        )
