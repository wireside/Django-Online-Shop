from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import static


urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("download/", include("download.urls")),
    path("feedback/", include("feedback.urls")),
    path("rating/", include("rating.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        static.serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
