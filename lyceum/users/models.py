import django.contrib.auth.models
import django.db.models
import sorl.thumbnail

from lyceum.s3_storage import MediaStorage

__all__ = ["Profile"]


class UserManager(django.contrib.auth.models.UserManager):
    CANONICAL_DOMAINS = {
        "ya.ru": "yandex.ru",
    }
    DOTS = {
        "yandex.ru": "-",
        "gmail.com": "",
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        profile = django.contrib.auth.models.User.profile
        profile_related = profile.related.name
        return queryset.select_related(
            profile_related,
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        normalized_email = self.normalize_email(mail)
        return self.active().get(email=normalized_email)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            email_name, _ = email_name.split("+", 1)

            domain_part = cls.CANONICAL_DOMAINS.get(domain_part, domain_part)

            email_name = email_name.replace(
                ".",
                cls.DOTS.get(domain_part, "."),
            )
        except ValueError:
            pass
        else:
            email = "@".join([email_name, domain_part.lower()])

        return email


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True


class Profile(django.db.models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

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
    coffee_count = django.db.models.PositiveIntegerField(
        verbose_name="чашки кофе",
        default=0,
    )
    image = django.db.models.ImageField(
        verbose_name="изображение профиля",
        upload_to=image_path,
        null=True,
        blank=True,
        storage=MediaStorage(),
    )
    attempts_count = django.db.models.PositiveIntegerField(
        verbose_name="попыток входа",
        default=0,
    )
    block_date = django.db.models.DateTimeField(
        verbose_name="дата блокировки",
        blank=True,
        null=True,
    )

    def get_image_300x300(self):
        if self.image:
            return sorl.thumbnail.get_thumbnail(
                self.image,
                "300x300",
                crop="center",
                quality=51,
            )

        return None

    def get_image_50x50(self):
        if self.image:
            return sorl.thumbnail.get_thumbnail(
                self.image,
                "50x50",
                crop="center",
                quality=51,
            )

        return None

    def __str__(self):
        return f"Профиль пользователя {self.user.username}."

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
