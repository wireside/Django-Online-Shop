# Generated by Django 4.2.16 on 2024-11-22 17:59

from django.db import migrations, models
import lyceum.s3_storage
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.user",),
            managers=[
                ("objects", users.models.UserManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name="profile",
            options={
                "verbose_name": "Профиль пользователя",
                "verbose_name_plural": "Профили пользователей",
            },
        ),
        migrations.AddField(
            model_name="profile",
            name="attempts_count",
            field=models.PositiveIntegerField(
                default=0, verbose_name="попыток входа"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=lyceum.s3_storage.MediaStorage(),
                upload_to=users.models.Profile.image_path,
                verbose_name="изображение профиля",
            ),
        ),
    ]