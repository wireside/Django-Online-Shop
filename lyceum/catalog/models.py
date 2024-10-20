import django.core.exceptions
import django.core.validators
import django.db
import django.db.models


def custom_validator(value):
    if "превосходно" not in value and "роскошно" not in value:
        raise django.core.exceptions.ValidationError(
            "В тексте должно быть слово `превосходно`",
        )


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        "Опубликовано",
        default=True,
    )
    name = django.db.models.TextField(
        "Название",
        help_text="max 150 символов",
        validators=[
            django.core.validators.MaxLengthValidator(150),
        ],
    )

    class Meta:
        abstract = True


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        unique=True,
        verbose_name="Слаг",
        validators=[
            django.core.validators.MaxLengthValidator(200),
        ],
    )
    weight = django.db.models.IntegerField(
        default=100,
        verbose_name="Вес",
        help_text="Вес должен быть больше 0 и меньше 32768",
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32768),
        ],
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name[:15]


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        unique=True,
        verbose_name="Слаг",
        help_text="Слаг содержит только латинские буквы,"
        " символы тире или нижнего подчеркивания"
        "и цифры",
        validators=[
            django.core.validators.MaxLengthValidator(200),
        ],
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name[:30]


class Item(AbstractModel):
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="catalog_items",
        verbose_name="Категория",
        default=1,
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="catalog_items",
    )
    text = django.db.models.TextField(
        verbose_name="Описание",
        help_text="Описание должно содержать строку,"
        " содержащую в себе `превосходно`"
        " или `роскошно` ",
        validators=[
            custom_validator,
        ],
        default="роскошно превосходно",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name[:15]
