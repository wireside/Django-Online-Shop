from django.db import models

class ItemManager(models.Manager):
    def on_main(self):
        # Выбираем только необходимые поля для отображения на главной странице
        return (
            super().get_queryset()
            .filter(is_published=True, is_on_main=True)
            .order_by('name')
        )

    def published(self):
        # Выбираем только необходимые поля для отображения на странице списка товаров
        return (
            super().get_queryset()
            .filter(is_published=True)
            .order_by('name')
        )