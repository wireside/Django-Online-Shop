import django.urls
import feedback.views

app_name = "feedback"

urlpatterns = [
    django.urls.path("", feedback.views.index, name="feedback"),
]
