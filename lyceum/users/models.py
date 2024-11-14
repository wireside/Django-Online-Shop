import django.contrib.auth.models
import django.db.models

__all__ = ["Profile"]


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="profile",
    )
    birthday = django.db.models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
    )
    image = django.db.models.ImageField(
        verbose_name="аватарка",
        upload_to="users/profile_pics/",
        blank=True,
        null=True,
    )
    coffee_count = django.db.models.IntegerField(
        verbose_name="счетчик переходов по /coffee",
        default=0,
    )

    class Meta:
        verbose_name = "профиль"
