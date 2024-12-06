import django.shortcuts
import django.views.generic

import cart.models
import catalog.models

__all__ = [
    "CartAddView",
    "CartClearView",
    "CartDeleteView",
    "CartDetailView",
    "CartUpdateView",
]


class CartDetailView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return django.shortcuts.redirect("users:login")

        template_name = "cart/cart.html"
        user_cart = django.shortcuts.get_object_or_404(
            cart.models.Cart.objects.detail(),
            user=self.request.user,
        )
        context = {"cart": user_cart}

        return django.shortcuts.render(request, template_name, context)


class CartUpdateView(django.views.generic.View):
    def post(self, request, item_id, flag):
        flag = int(flag)

        cart_item = django.shortcuts.get_object_or_404(
            cart.models.CartItem,
            id=item_id,
        )
        if flag == 0:
            cart_item.quantity -= 1

        cart_item.quantity += flag
        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

        return django.shortcuts.redirect("cart:cart")


class CartAddView(django.views.generic.View):
    def post(self, request, item_id):
        user_cart = request.user.cart

        item = django.shortcuts.get_object_or_404(
            catalog.models.Item,
            id=item_id,
            is_published=True,
        )
        cart_item, created = cart.models.CartItem.objects.get_or_create(
            cart=user_cart,
            item=item,
        )

        if not created:
            cart_item.quantity += 1

        cart_item.save()

        return django.shortcuts.redirect("catalog:item_detail", pk=item_id)


class CartDeleteView(django.views.generic.View):
    def post(self, request, item_id):
        user_cart = request.user.cart

        cart_item = django.shortcuts.get_object_or_404(
            cart.models.CartItem,
            cart=user_cart,
            item_id=item_id,
        )

        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        return django.shortcuts.redirect("catalog:item_detail", pk=item_id)


class CartClearView(django.views.generic.View):
    def post(self, request):
        user_cart = request.user.cart
        user_cart.items.all().delete()

        return django.shortcuts.redirect("cart:cart")
