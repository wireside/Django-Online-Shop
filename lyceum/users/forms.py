import django.contrib.auth.forms
import django.forms

import users.models


class BootstrapFormMixin(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control shadow-sm"


class UserCreationForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.email.field.name,
            users.models.User.username.field.name,
        )


class UserChangeForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserChangeForm,
):
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
        )


class UpdateProfileForm(
    BootstrapFormMixin,
    django.forms.ModelForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[users.models.Profile.coffee_count.field.name].disabled = (
            True
        )

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.image.field.name,
            users.models.Profile.birthday.field.name,
            users.models.Profile.coffee_count.field.name,
        )
        help_texts = {
            users.models.Profile.birthday.field.name: "Формат: гггг-мм-дд",
        }
