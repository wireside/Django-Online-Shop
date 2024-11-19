import django.forms

import rating.models

__all__ = ["BootstrapForm", "RatingForm"]


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["score"].choices = [
            (k, v) for k, v in self.fields["score"].choices if k
        ]


class RatingForm(BootstrapForm):
    class Meta:
        model = rating.models.Rating
        fields = (rating.models.Rating.score.field.name,)
        labels = {
            rating.models.Rating.score.field.name: "Оценка товара",
        }
        widgets = {
            rating.models.Rating.score.field.name: django.forms.RadioSelect(
                attrs={"class": "form-check-inline"},
            ),
        }
