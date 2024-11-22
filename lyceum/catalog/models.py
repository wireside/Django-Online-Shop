import django.core.exceptions
import django.core.validators
import django.db
import django.db.models
from django.utils.safestring import mark_safe
import django_ckeditor_5.fields


import catalog.managers
import catalog.validators
import core.models

__all__ = ["Category", "Image", "Item", "MainImage", "Tag"]


class Category(core.models.BaseModel):
    objects = catalog.managers.CategoryManager()

    slug = django.db.models.SlugField(
        unique=True,
        verbose_name="слаг",
        help_text="Максимум 200 символов",
        validators=[
            django.core.validators.MaxLengthValidator(200),
        ],
    )
    weight = django.db.models.PositiveSmallIntegerField(
        default=100,
        verbose_name="вес",
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
        return self.name[:15]


class Tag(core.models.BaseModel):
    slug = django.db.models.SlugField(
        unique=True,
        verbose_name="слаг",
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
        return self.name[:30]


class Item(django.db.models.Model):
    objects = catalog.managers.ItemManager()

    is_published = django.db.models.BooleanField(
        verbose_name="опубликовано",
        default=True,
    )
    is_on_main = django.db.models.BooleanField(
        verbose_name="на главной странице",
        default=False,
    )
    name = django.db.models.CharField(
        verbose_name="название",
        max_length=150,
        help_text="Максимум 150 символов",
    )
    category = django.db.models.ForeignKey(
        Category,
        null=True,
        on_delete=django.db.models.SET_NULL,
        verbose_name="категория",
        help_text="Выберите категорию",
        related_name="items",
        related_query_name="items",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        related_query_name="items",
    )
    text = django_ckeditor_5.fields.CKEditor5Field(
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
    updated = django.db.models.DateTimeField(
        verbose_name="время изменения",
        auto_now=True,
        null=True,
        blank=True,
    )
    created = django.db.models.DateTimeField(
        verbose_name="время создания",
        auto_now_add=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("-is_published",)
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    def __str__(self):
        return self.name[:15]

    def image_tmb(self):
        if self.main_image.image:
            return mark_safe(
                f"<img src='{self.main_image.get_image_50x50.url}'>",
            )

        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class MainImage(core.models.ImageBaseModel):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
    )

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class Image(core.models.ImageBaseModel):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="images",
    )

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"
