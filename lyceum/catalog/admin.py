import django.contrib.admin

from catalog import models


django.contrib.admin.site.register(models.Category)
django.contrib.admin.site.register(models.Tag)


@django.contrib.admin.register(models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        models.Item.is_published.field.name,
        models.Item.name.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = (models.Item.name.field.name,)
    filter_horizontal = (models.Item.tags.field.name,)

