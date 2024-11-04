from django.db import models


class ItemManager(models.Manager):
    def on_main(self):
        return (
            super()
            .get_queryset()
            .filter(is_published=True, is_on_main=True)
            .order_by("name")
        )

    def published(self):
        return (
            super().get_queryset()
            .filter(is_published=True)
            .order_by("name")
        )
