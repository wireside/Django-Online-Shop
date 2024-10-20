from django.urls import path

from homepage import views

urlpatterns = [
    path("", views.home),
    path("coffee", views.coffee),
    path("coffee/", views.coffee),
]
