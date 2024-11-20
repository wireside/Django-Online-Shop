# Generated by Django 4.2.16 on 2024-10-31 00:21

import catalog.validators
import django.core.validators
from django.db import migrations, models


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
    ]
