import django.forms

from feedback.models import Feedback


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"
        labels = {
            Feedback.name.field.name: "Имя",
            Feedback.text.field.name: "Сообщение",
            Feedback.mail.field.name: "Почта",
        }
        help_texts = {
            "name": "Введите ваше имя",
        }
        error_messages = {
            "name": {
                "max_length": "Имя слишком длинное",
            },
        }
        widgets = {
            "name": django.forms.TextInput(attrs={"class": "form-control"}),
            "text": django.forms.Textarea(attrs={"class": "form-control"}),
            "mail": django.forms.EmailInput(attrs={"class": "form-control"}),
        }
