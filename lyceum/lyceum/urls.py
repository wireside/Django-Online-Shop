import django.views.static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
