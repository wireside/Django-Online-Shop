# Generated by Django 4.2.16 on 2024-11-08 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_alter_image_image_alter_mainimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                help_text="Выберите категорию",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.category",
                verbose_name="категория",
            ),
        ),
    ]