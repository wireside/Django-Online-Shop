# Generated by Django 4.2.16 on 2024-10-21 18:39

import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("catalog", "0001_initial"),
        ("catalog", "0002_alter_item_text"),
        ("catalog", "0003_alter_item_text"),
        ("catalog", "0004_last_migration"),
    ]

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Максимум 200 символов",
                        unique=True,
                        validators=[
                            django.core.validators.MaxLengthValidator(200)
                        ],
                        verbose_name="cлаг",
                    ),
                ),
                (
                    "weight",
                    models.PositiveSmallIntegerField(
                        default=100,
                        help_text="Вес должен быть больше 0 и меньше 32768",
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="Значение должно быть больше 0"
                            ),
                            django.core.validators.MaxValueValidator(
                                32767,
                                message="Значение должно быть меньше 32767",
                            ),
                        ],
                        verbose_name="Вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
                "ordering": ("weight", "id"),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Максимум 200 символов",
                        unique=True,
                        validators=[
                            django.core.validators.MaxLengthValidator(200)
                        ],
                        verbose_name="cлаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
                "ordering": ("slug",),
                "default_related_name": "tags",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимум 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Описание должно содержать слова 'превосходно' или 'роскошно'",
                        validators=[
                            catalog.validators.WordsValidator(
                                "роскошно", "превосходно"
                            )
                        ],
                        verbose_name="описание",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Выберите категорию",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.category",
                        verbose_name="категория",
                    ),
                ),
                ("tags", models.ManyToManyField(to="catalog.tag")),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
                "default_related_name": "items",
            },
        ),
    ]
