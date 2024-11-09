import django.db.models


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name="имя",
        max_length=50,
        help_text="Имя пользователя должно быть меньше 50 символов",
    )
    text = django.db.models.TextField(
        verbose_name="текстовое поле",
        help_text="Текст письма",
    )
    created_on = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата и время создания",
    )
    mail = django.db.models.EmailField(verbose_name="почта")
