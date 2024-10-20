import django.contrib.admin

import catalog.models


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.name.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.is_published.field.name,
        catalog.models.Category.name.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.is_published.field.name,
        catalog.models.Tag.name.field.name,
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
