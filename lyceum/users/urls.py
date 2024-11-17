import django.contrib.auth.views
import django.urls


app_name = "users"

login_view = django.contrib.auth.views.LoginView.as_view(
    template_name="users/login.html",
)
logout_view = django.contrib.auth.views.LogoutView.as_view(
    next_page="login",
)
password_reset_view = django.contrib.auth.views.PasswordResetView.as_view(
    template_name="users/password_reset.html",
)
password_reset_done_view = (
    django.contrib.auth.views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html",
    )
)


urlpatterns = [
    django.urls.path(
        "login/",
        login_view,
        name="login",
    ),
    django.urls.path(
        "logout/",
        logout_view,
        name="logout",
    ),
    django.urls.path(
        "password_reset/",
        password_reset_view,
    ),
    django.urls.path(
        "password_reset/done/",
        password_reset_done_view,
        name="password_reset_done",
    ),
]
