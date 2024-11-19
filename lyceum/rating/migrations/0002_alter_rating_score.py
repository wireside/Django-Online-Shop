# Generated by Django 4.2.16 on 2024-11-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rating", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="score",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "Ненависть"),
                    (2, "Неприязнь"),
                    (3, "Нейтрально"),
                    (4, "Обожание"),
                    (5, "Любовь"),
                ]
            ),
        ),
    ]
