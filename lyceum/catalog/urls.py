from django.urls import path, re_path, register_converter

from catalog import converters, views

register_converter(converters.PositiveIntegerConverter, "positive")

urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    path("converter/<positive:pk>/", views.item_positive_converter),
    re_path(r"^re/(?P<pk>\d*[1-9]\d*)/$", views.item_customer_converter),
]
