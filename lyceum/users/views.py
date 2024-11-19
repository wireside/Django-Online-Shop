import datetime

import django.conf
import django.contrib.auth.decorators
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.utils.timezone

import users.forms
import users.models

__all__ = [
    "activate",
    "profile",
    "reactivate",
    "signup",
    "user_detail",
    "user_list",
]


def signup(request):
    user_form = users.forms.UserCreationForm(request.POST or None)
    context = {"user_form": user_form}
    if request.method == "POST" and user_form.is_valid():
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data["password1"])
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        user_profile = users.models.Profile(user=user)
        user_profile.save()

        activate_url = django.urls.reverse("users:activate", args=[user.id])
        activation_link = f"{request.build_absolute_uri(activate_url)}"
        django.core.mail.send_mail(
            subject="Активация аккаунта",
            message=(
                f"Для активации аккаунта перейдите"
                f" по ссылке: {activation_link}"
            ),
            from_email=django.conf.settings.MAIL,
            recipient_list=[user.email],
        )

        return django.shortcuts.redirect("users:login")

    return django.shortcuts.render(request, "users/signup.html", context)


def activate(request, pk):
    user = users.models.User.objects.get(pk=pk)
    if (
        user.date_joined + datetime.timedelta(hours=12)
        > django.utils.timezone.now()
    ):
        user.is_active = True
        user.save()

    return django.shortcuts.redirect(django.urls.reverse("homepage:home"))


def reactivate(request, pk):
    user = users.models.User.objects.get(pk=pk)
    if (
        user.profile.block_date + datetime.timedelta(days=7)
        > django.utils.timezone.now()
    ):
        user.is_active = True
        user.save()

    return django.shortcuts.redirect(django.urls.reverse("homepage:home"))


def user_list(request):
    context = {"users": users.models.User.objects.active()}

    return django.shortcuts.render(request, "users/user_list.html", context)


def user_detail(request, pk: int):
    searched_user = django.shortcuts.get_object_or_404(
        users.models.User.objects.active(),
        pk=pk,
    )

    context = {"user": searched_user}

    return django.shortcuts.render(request, "users/user_detail.html", context)


@django.contrib.auth.decorators.login_required
def profile(request):
    user_form = users.forms.UserChangeForm(
        request.POST or None,
        instance=request.user,
    )
    profile_form = users.forms.UpdateProfileForm(
        request.POST or None,
        instance=request.user.profile,
    )
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    if (
        request.method == "POST"
        and user_form.is_valid()
        and profile_form.is_valid()
    ):
        user_form.save()
        profile_form.save()
        django.contrib.messages.success(request, "Изменения сохранены")
        return django.shortcuts.redirect(django.urls.reverse("users:profile"))

    return django.shortcuts.render(request, "users/profile.html", context)
