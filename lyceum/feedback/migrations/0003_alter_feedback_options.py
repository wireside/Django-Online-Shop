# Generated by Django 4.2.16 on 2024-11-11 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "feedback",
            "0002_remove_feedback_mail_remove_feedback_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="feedback",
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
    ]