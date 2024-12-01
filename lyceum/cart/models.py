import django.db.models
from django.utils.safestring import mark_safe

import catalog.models
import users.models

__all__ = ["Cart", "CartItem"]


class Cart(django.db.models.Model):
    user = django.db.models.OneToOneField(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="cart",
        verbose_name="пользователь",
        unique=True,
    )
    updated = django.db.models.DateTimeField(
        verbose_name="время изменения",
        auto_now=True,
        null=True,
        blank=True,
    )
    created = django.db.models.DateTimeField(
        verbose_name="время создания",
        auto_now_add=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        default_related_name = "carts"

    def __str__(self):
        return "Корзина пользователя " + str(self.user.username)

    def get_total_price(self):
        return sum(item.get_price() for item in self.items.all())

    get_total_price.short_description = "К оформлению"


class CartItem(django.db.models.Model):
    cart = django.db.models.ForeignKey(
        Cart,
        on_delete=django.db.models.CASCADE,
        related_name="items",
    )
    item = django.db.models.ForeignKey(
        catalog.models.Item,
        on_delete=django.db.models.CASCADE,
        related_name="cart_items",
        verbose_name="товар",
    )
    quantity = django.db.models.PositiveIntegerField(
        verbose_name="количество",
        default=1,
    )

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"
        unique_together = (("cart", "item"),)

    def __str__(self):
        output = str(self.cart) + " : " + str(self.item.name)
        output += "(" + str(self.quantity) + ")"
        return output

    def get_price(self):
        return self.item.price * self.quantity

    def show_price(self):
        return mark_safe(
            f"<p>{self.get_price()}</p>",
        )

    show_price.short_description = "Полная стоимость"
    show_price.allow_tags = True
