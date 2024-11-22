import django.urls

import feedback.views

app_name = "feedback"

urlpatterns = [
    django.urls.path("", feedback.views.IndexView.as_view(), name="feedback"),
]
