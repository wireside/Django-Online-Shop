import time

import django.conf
import django.db.models

from lyceum.s3_storage import MediaStorage


storage = None

if not django.conf.settings.DEBUG:
    storage = MediaStorage()


class Feedback(django.db.models.Model):
    class Status(django.db.models.TextChoices):
        NEW = "new", "New"
        WIP = "wip", "Work in progress"
        ANS = "ans", "Answered"

    text = django.db.models.TextField(
        verbose_name="текстовое поле",
    )
    created_on = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата и время создания",
    )
    status = django.db.models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.NEW,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.text[:50]


class FeedbackAuthor(django.db.models.Model):
    feedback = django.db.models.OneToOneField(
        Feedback,
        related_name="author",
        on_delete=django.db.models.CASCADE,
    )
    name = django.db.models.CharField(
        verbose_name="имя",
        max_length=50,
    )
    mail = django.db.models.EmailField(verbose_name="электронная почта")


class FeedbackFile(django.db.models.Model):
    def get_path(self, filename):
        return f"uploads/{self.feedback_id}/{time.time()}_{filename}"

    feedback = django.db.models.ForeignKey(
        Feedback,
        related_name="files",
        on_delete=django.db.models.CASCADE,
    )
    file = django.db.models.FileField(
        verbose_name="файл",
        upload_to=get_path,
        blank=True,
        storage=storage,
    )
