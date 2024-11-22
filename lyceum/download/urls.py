import django.urls

import download.views

app_name = "download"

urlpatterns = [
    django.urls.path(
        "<path:path>",
        download.views.FileDownloadView.as_view(),
        name="file",
    ),
]
