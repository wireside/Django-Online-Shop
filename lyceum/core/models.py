import re

import django.core.exceptions
import django.db.models
import transliterate


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
