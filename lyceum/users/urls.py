import django.contrib.auth.views
import django.urls


app_name = "users"

login_view = django.contrib.auth.views.LoginView.as_view(
    template_name="users/login.html",
)

urlpatterns = [
    django.urls.path(
        "login/",
        login_view,
        name="login",
    ),
]
