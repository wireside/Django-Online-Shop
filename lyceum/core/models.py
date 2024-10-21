import re

# import django.core.exceptions
import django.db.models

# import transliterate


ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


class BaseModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        verbose_name="опубликовано",
        default=True,
    )
    name = django.db.models.CharField(
        verbose_name="название",
        max_length=150,
        help_text="Максимум 150 символов",
        unique=True,
    )

    class Meta:
        abstract = True
