from django.urls import path

from catalog import views


app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("new/", views.new, name="item_new"),
    path("friday/", views.friday, name="item_friday"),
    path("unverified/", views.unverified, name="item_unverified"),
]
