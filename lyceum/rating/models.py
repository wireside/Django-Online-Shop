import django.db.models

import catalog.models
import users.models

__all__ = ["Rating"]


class Rating(django.db.models.Model):
    SCORE_CHOICES = [
        (1, "1 - Ненависть"),
        (2, "2 - Неприязнь"),
        (3, "3 - Нейтрально"),
        (4, "4 - Обожание"),
        (5, "5 - Любовь"),
    ]

    user = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="rating",
    )
    item = django.db.models.ForeignKey(
        catalog.models.Item,
        on_delete=django.db.models.CASCADE,
        related_name="rating",
    )
    score = django.db.models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES,
    )

    def __str__(self):
        return f"{self.score} - {self.item} - {self.user}"

    class Meta:
        unique_together = (
            "user",
            "item",
        )
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
