# Generated by Django 4.2.16 on 2024-11-21 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0006_alter_feedbackfile_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="statuslog",
            old_name="from_status",
            new_name="from",
        ),
        migrations.RenameField(
            model_name="statuslog",
            old_name="to_status",
            new_name="to",
        ),
    ]
