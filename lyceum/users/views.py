import datetime

import django
import django.conf
import django.contrib.auth.decorators
import django.contrib.auth.mixins
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.utils.timezone
import django.views.generic

import users.forms
import users.models

__all__ = []


class SignUpView(django.views.generic.FormView):
    template_name = "users/signup.html"
    form_class = users.forms.UserCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
            user.save()

            user_profile = users.models.Profile(user=user)
            user_profile.save()

            activate_url = django.urls.reverse(
                "users:activate",
                args=[user.id],
            )
            activation_link = (
                f"{self.request.build_absolute_uri(activate_url)}"
            )
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

        return self.render_to_response(
            self.get_context_data(user_form=form),
        )

    def get(self, request, *args, **kwargs):

        return self.render_to_response(
            self.get_context_data(user_form=self.form_class()),
        )


class ActiveView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        user = users.models.User.objects.get(pk=kwargs["pk"])

        if (
            user.date_joined + datetime.timedelta(hours=12)
            > django.utils.timezone.now()
        ):
            user.is_active = True
            user.save()

        return django.shortcuts.redirect(django.urls.reverse("homepage:home"))


class ReactiveView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        user = users.models.User.objects.get(pk=kwargs["pk"])

        if (
            user.profile.block_date + datetime.timedelta(days=7)
            > django.utils.timezone.now()
        ):
            user.is_active = True
            user.save()

        return django.shortcuts.redirect(django.urls.reverse("homepage:home"))


class UserListView(django.views.generic.ListView):
    template_name = "users/user_list.html"
    model = users.models.User

    def get_queryset(self):
        return users.models.User.objects.active()


class UserDetailView(django.views.generic.DetailView):
    template_name = "users/user_detail.html"
    model = users.models.User
    context_object_name = "user"

    def get_object(self, queryset=None):
        queryset = self.model.objects.active()
        return django.shortcuts.get_object_or_404(
            queryset,
            pk=self.kwargs["pk"],
        )


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    template_name = "users/profile.html"
    form_class = users.forms.UserChangeForm
    form_class2 = users.forms.UpdateProfileForm

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(
                user_form=self.form_class(
                    request.POST or None,
                    instance=request.user,
                ),
                profile_form=self.form_class2(
                    request.POST or None,
                    request.FILES or None,
                    instance=request.user.profile,
                ),
            ),
        )

    def post(self, request, *args, **kwargs):
        user_form = self.form_class(request.POST, instance=request.user)
        profile_form = self.form_class2(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            django.contrib.messages.success(request, "Изменения сохранены")

            return django.shortcuts.redirect(
                django.urls.reverse("users:profile"),
            )

        return self.render_to_response(
            self.get_context_data(
                user_form=user_form,
                profile_form=profile_form,
            ),
        )
