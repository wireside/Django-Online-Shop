import django.forms


class MultipleFileInput(django.forms.FileInput):
    allow_multiple_selected = True
