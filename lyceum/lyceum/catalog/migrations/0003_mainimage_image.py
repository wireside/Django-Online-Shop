# Generated by Django 4.2.16 on 2024-10-31 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0002_category_canonical_name_tag_canonical_name_and_more",
        ),
    ]

    operations = [
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
