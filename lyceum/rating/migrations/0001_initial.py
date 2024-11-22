# Generated by Django 4.2.16 on 2024-11-22 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog", "0006_alter_image_image_alter_mainimage_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rating",
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
                    "score",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "1 - Ненависть"),
                            (2, "2 - Неприязнь"),
                            (3, "3 - Нейтрально"),
                            (4, "4 - Обожание"),
                            (5, "5 - Любовь"),
                        ]
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating",
                        to="catalog.item",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оценка",
                "verbose_name_plural": "Оценки",
            },
        ),
    ]
