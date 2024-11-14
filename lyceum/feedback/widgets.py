import django.forms

__all__ = ["MultipleFileInput"]


class MultipleFileInput(django.forms.FileInput):
    allow_multiple_selected = True
