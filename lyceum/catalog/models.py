import django.core.exceptions
import django.core.validators
import django.db
import django.db.models

import catalog.validators
import core.models


class Category(core.models.BaseModel):
    slug = django.db.models.SlugField(
        unique=True,
        verbose_name="Слаг",
        help_text="Максимум 200 символов",
        validators=[
            django.core.validators.MaxLengthValidator(200),
        ],
    )
    weight = django.db.models.PositiveSmallIntegerField(
        default=100,
        verbose_name="Вес",
        help_text="Вес должен быть больше 0 и меньше 32768",
        validators=[
            django.core.validators.MinValueValidator(
                1,
                message="Значение должно быть больше 0",
            ),
            django.core.validators.MaxValueValidator(
                32767,
                message="Значение должно быть меньше 32767",
            ),
        ],
    )

    class Meta:
        ordering = (
            "weight",
            "id",
        )
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Tag(core.models.BaseModel):
    slug = django.db.models.SlugField(
        unique=True,
        verbose_name="Слаг",
        help_text="Максимум 200 символов",
        validators=[
            django.core.validators.MaxLengthValidator(200),
        ],
    )

    class Meta:
        ordering = ("slug",)
        verbose_name = "тег"
        verbose_name_plural = "теги"
        default_related_name = "tags"

    def __str__(self):
        return self.name


class Item(core.models.BaseModel):
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(Tag)
    text = django.db.models.TextField(
        verbose_name="описание",
        help_text=(
            "Описание должно содержать слова 'превосходно' или 'роскошно'"
        ),
        validators=[
            catalog.validators.WordsValidator(
                "роскошно",
                "превосходно",
            ),
        ],
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    def __str__(self):
        return self.name[:15]
