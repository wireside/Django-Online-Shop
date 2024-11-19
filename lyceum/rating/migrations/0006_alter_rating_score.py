# Generated by Django 4.2.16 on 2024-11-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rating", "0005_alter_rating_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="score",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "1 - Ненависть"),
                    (2, "2 - Неприязнь"),
                    (3, "3 - Нейтрально"),
                    (4, "4 - Обожание"),
                    (5, "5 - Любовь"),
                ]
            ),
        ),
    ]
