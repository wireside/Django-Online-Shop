import django.urls

import rating.views


app_name = "rating"


urlpatterns = [
    django.urls.path(
        "delete/<int:pk>",
        rating.views.DeleteView.as_view(),
        name="delete",
    ),
]
