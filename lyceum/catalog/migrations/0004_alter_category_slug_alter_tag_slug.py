# Generated by Django 4.2.16 on 2024-10-21 18:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_item_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Максимум 200 символов",
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(200)],
                verbose_name="cлаг",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                help_text="Максимум 200 символов",
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(200)],
                verbose_name="cлаг",
            ),
        ),
    ]
