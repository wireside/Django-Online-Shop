# Generated by Django 4.2.16 on 2024-11-18 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0004_user"),
        ("catalog", "0011_alter_item_created_alter_item_updated"),
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
                        blank=True,
                        choices=[
                            (1, "Ненависть"),
                            (2, "Неприязнь"),
                            (3, "Нейтрально"),
                            (4, "Обожание"),
                            (5, "Любовь"),
                        ],
                        null=True,
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
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating",
                        to="users.user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оценка",
                "verbose_name_plural": "Оценки",
                "unique_together": {("user", "item")},
            },
        ),
    ]