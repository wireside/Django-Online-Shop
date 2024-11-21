import django.conf
import django.contrib.auth.backends
import django.core.mail
import django.urls
import django.utils
import django.utils.timezone


import users.models

__all__ = ["AuthBackend"]


class AuthBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            return None

        if user.is_superuser and not user.profile:
            users.models.Profile.objects.create(user=user)

        if user.check_password(password):
            user.profile.attempts_count = 0
            user.profile.save()
            return user

        user.profile.attempts_count += 1
        if (
            user.profile.attempts_count
            >= django.conf.settings.MAX_AUTH_ATTEMPTS
        ):
            user.is_active = False
            user.profile.block_date = django.utils.timezone.now()
            user.save()
            activate_url = django.urls.reverse(
                "users:reactivate",
                kwargs={"pk": user.id},
            )
            django.core.mail.send_mail(
                f"Привет {user.username}",
                "Мы заметили подозрительную актвиность."
                "Из-за этого заблокировали аккаунт."
                "Для разблокировки перейдите по ссылке "
                "(действительна в течении недели)"
                f"{activate_url}",
                django.conf.settings.MAIL,
                [user.email],
                fail_silently=False,
            )

        user.profile.save()

        return None
