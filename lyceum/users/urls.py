import django.contrib.auth.views
import django.urls

import users.views

app_name = "users"

login_view = django.contrib.auth.views.LoginView.as_view(
    template_name="users/login.html",
)
logout_view = django.contrib.auth.views.LogoutView.as_view(
    template_name="users/logout.html",
)
password_change_view = django.contrib.auth.views.PasswordChangeView.as_view(
    template_name="users/password_change.html",
)
password_change_done_view = (
    django.contrib.auth.views.PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html",
    )
)
password_reset_view = django.contrib.auth.views.PasswordResetView.as_view(
    template_name="users/password_reset.html",
)
password_reset_done_view = (
    django.contrib.auth.views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html",
    )
)
password_reset_confirm_view = (
    django.contrib.auth.views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
    )
)
password_reset_complete_view = (
    django.contrib.auth.views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html",
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
        "password_change/",
        password_change_view,
        name="password_change",
    ),
    django.urls.path(
        "password_change/done/",
        password_change_done_view,
        name="password_change_done",
    ),
    django.urls.path(
        "password_reset/",
        password_reset_view,
        name="password_reset",
    ),
    django.urls.path(
        "password_reset/done/",
        password_reset_done_view,
        name="password_reset_done",
    ),
    django.urls.path(
        "reset/<uidb64>/<token>/",
        password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    django.urls.path(
        "reset/done/",
        password_reset_complete_view,
        name="password_reset_complete",
    ),
    django.urls.path(
        "signup/",
        users.views.signup,
        name="signup",
    ),
    django.urls.path(
        "users/",
        users.views.user_list,
        name="user_list",
    ),
    django.urls.path(
        "user/<pk>/",
        users.views.user_detail,
        name="user_detail",
    ),
    django.urls.path(
        "activate/<pk>/",
        users.views.activate,
        name="activate",
    ),
    django.urls.path(
        "reactivate/<pk>/",
        users.views.reactivate,
        name="reactivate",
    ),
]
