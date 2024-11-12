import django.forms


class EchoForm(django.forms.Form):
    text = django.forms.CharField(
        widget=django.forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Какой-то текст...",
            },
        ),
        label="Текст",
    )
