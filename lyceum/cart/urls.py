import django.urls

import cart.views


app_name = "cart"

urlpatterns = [
    django.urls.path(
        "",
        cart.views.CartDetailView.as_view(),
        name="cart",
    ),
    django.urls.re_path(
        r"^(?P<item_id>\d+)/update/(?P<flag>[01])/$",
        cart.views.CartUpdateView.as_view(),
        name="update",
    ),
    django.urls.path(
        "add/<int:item_id>/",
        cart.views.CartAddView.as_view(),
        name="add",
    ),
    django.urls.path(
        "delete/<int:item_id>/",
        cart.views.CartDeleteView.as_view(),
        name="delete",
    ),
    django.urls.path(
        "clear/",
        cart.views.CartClearView.as_view(),
        name="clear",
    ),
]
