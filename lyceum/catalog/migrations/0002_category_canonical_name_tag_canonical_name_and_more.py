# Generated by Django 4.2.16 on 2024-10-30 23:02

import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="canonical_name",
            field=models.CharField(
                editable=False,
                help_text="Каноническое название элемента",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="каноническое название",
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="canonical_name",
            field=models.CharField(
                editable=False,
                help_text="Каноническое название элемента",
                max_length=150,
                null=True,
                unique=True,
                verbose_name="каноническое название",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Максимум 200 символов",
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(200)],
                verbose_name="слаг",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="weight",
            field=models.PositiveSmallIntegerField(
                default=100,
                help_text="Вес должен быть больше 0 и меньше 32768",
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="Значение должно быть больше 0"
                    ),
                    django.core.validators.MaxValueValidator(
                        32767, message="Значение должно быть меньше 32767"
                    ),
                ],
                verbose_name="вес",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(
                help_text="Максимум 150 символов",
                max_length=150,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="Описание должно содержать слова 'превосходно' или 'роскошно'",
                validators=[
                    catalog.validators.WordsValidator(
                        "роскошно", "превосходно"
                    )
                ],
                verbose_name="описание",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                help_text="Максимум 200 символов",
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(200)],
                verbose_name="слаг",
            ),
        ),
        migrations.CreateModel(
            name="MainImage",
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
                    "image",
                    models.ImageField(
                        default=None,
                        upload_to="catalog/",
                        verbose_name="изображение",
                    ),
                ),
                (
                    "item",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="main_image",
                        to="catalog.item",
                    ),
                ),
            ],
            options={
                "verbose_name": "главное изображение",
                "verbose_name_plural": "главные изображения",
            },
        ),
        migrations.CreateModel(
            name="Image",
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
                    "image",
                    models.ImageField(
                        default=None,
                        upload_to="catalog/",
                        verbose_name="изображение",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="catalog.item",
                    ),
                ),
            ],
            options={
                "verbose_name": "фото",
                "verbose_name_plural": "фото",
            },
        ),
    ]
