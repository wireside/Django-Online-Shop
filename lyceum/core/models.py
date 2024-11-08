import re

import django.core.exceptions
import django.db.models
from django.conf import settings
import sorl.thumbnail
import transliterate

from lyceum.s3_storage import MediaStorage


storage = None

if not settings.DEBUG:
    storage = MediaStorage()

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

    canonical_name = django.db.models.CharField(
        max_length=150,
        null=True,
        unique=True,
        editable=False,
        verbose_name="каноническое название",
        help_text="Каноническое название элемента",
    )

    def _generate_canonical_name(self):
        try:
            transliterated = transliterate.translit(
                self.name.lower(),
                reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            transliterated = self.name.lower()

        return ONLY_LETTERS_REGEX.sub(
            "",
            transliterated,
        )

    def save(self, *args, **kwargs):
        self.canonical_name = self._generate_canonical_name()
        super().save(*args, **kwargs)

    def clean(self):
        self.canonical_name = self._generate_canonical_name()
        if (
            type(self)
            .objects.filter(canonical_name=self.canonical_name)
            .exclude(id=self.id)
            .count()
        ) > 0:
            raise django.core.exceptions.ValidationError(
                "Уже есть такой же элемент",
            )

    class Meta:
        abstract = True


class ImageBaseModel(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to="catalog/",
        default=None,
        storage=storage,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def get_image_600x600(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "600x600",
            crop="center",
            quality=90,
        )

    @property
    def get_image_50x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "50x50",
            crop="center",
            quality=51,
        )

    def __str__(self):
        return self.item.name

    class Meta:
        abstract = True
