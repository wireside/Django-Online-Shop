import django.contrib.admin

import cart.models


__all__ = []


@django.contrib.admin.register(cart.models.CartItem)
class CartItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        cart.models.CartItem.item.field.name,
        cart.models.CartItem.cart.field.name,
        cart.models.CartItem.quantity.field.name,
        cart.models.CartItem.show_price,
    )
    list_display_links = (
        cart.models.CartItem.item.field.name,
        cart.models.CartItem.cart.field.name,
    )


class CartItem(django.contrib.admin.TabularInline):
    model = cart.models.CartItem
    fields = (
        cart.models.CartItem.item.field.name,
        cart.models.CartItem.quantity.field.name,
    )


@django.contrib.admin.register(cart.models.Cart)
class CartAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        cart.models.Cart.user.field.name,
        cart.models.Cart.get_total_price,
        cart.models.Cart.created.field.name,
        cart.models.Cart.updated.field.name,
    )
    list_display_links = (cart.models.Cart.user.field.name,)
    inlines = (CartItem,)
