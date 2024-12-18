# Generated by Django 4.2.16 on 2024-11-22 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_alter_image_image_alter_mainimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                related_query_name="images",
                to="catalog.item",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                help_text="Выберите категорию",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="items",
                related_query_name="items",
                to="catalog.category",
                verbose_name="категория",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(
                related_name="items",
                related_query_name="items",
                to="catalog.tag",
            ),
        ),
    ]
