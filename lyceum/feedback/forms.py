import django.forms

import feedback.models
import feedback.widgets

__all__ = [
    "BootstrapForm",
    "FeedbackAuthorForm",
    "FeedbackFileForm",
    "FeedbackForm",
]


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            field.field.widget.attrs["placeholder"] = field.help_text


class FeedbackAuthorForm(BootstrapForm):
    class Meta:
        model = feedback.models.FeedbackAuthor
        fields = (
            feedback.models.FeedbackAuthor.name.field.name,
            feedback.models.FeedbackAuthor.mail.field.name,
        )
        labels = {
            feedback.models.FeedbackAuthor.name.field.name: "Имя",
            feedback.models.FeedbackAuthor.mail.field.name: (
                "Электронная почта"
            ),
        }
        help_texts = {
            feedback.models.FeedbackAuthor.name.field.name: "Введите ваше имя",
            feedback.models.FeedbackAuthor.mail.field.name: "mail@example.com",
        }


class FeedbackFileForm(BootstrapForm):
    class Meta:
        model = feedback.models.FeedbackFile
        fields = {
            feedback.models.FeedbackFile.file.field.name,
        }
        help_texts = {
            feedback.models.FeedbackFile.file.field.name: (
                "При необходимости прикрепите файлы"
            ),
        }
        widgets = {
            feedback.models.FeedbackFile.file.field.name: (
                feedback.widgets.MultipleFileInput(
                    attrs={
                        "class": "form-control",
                        "type": "file",
                        "multiple": True,
                    },
                )
            ),
        }


class FeedbackForm(BootstrapForm):
    class Meta:
        model = feedback.models.Feedback
        exclude = (
            feedback.models.Feedback.id.field.name,
            feedback.models.Feedback.status.field.name,
            feedback.models.Feedback.created_on.field.name,
        )
        fields = (feedback.models.Feedback.text.field.name,)
        labels = {
            feedback.models.Feedback.text.field.name: "Сообщение",
        }
        help_texts = {
            feedback.models.Feedback.text.field.name: (
                "Введите текст сообщения"
            ),
        }
