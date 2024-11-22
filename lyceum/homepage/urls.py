from django.urls import path

from homepage import views


app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("echo/", views.echo, name="echo"),
    path("echo/submit/", views.echo_submit, name="echo_submit"),
    path("coffee/", views.coffee, name="coffee"),
]
