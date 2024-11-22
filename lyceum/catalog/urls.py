from django.urls import path

from catalog import views


app_name = "catalog"

urlpatterns = [
    path("", views.ItemListView.as_view(), name="item_list"),
    path("<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("new/", views.NewItemsView.as_view(), name="item_new"),
    path("friday/", views.FridayView.as_view(), name="item_friday"),
    path(
        "unverified/",
        views.UnverifiedView.as_view(),
        name="item_unverified",
    ),
]
