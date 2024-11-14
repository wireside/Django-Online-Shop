import django.conf
import django.http

__all__ = ["file"]


def file(request, path):
    return django.http.FileResponse(
        open(django.conf.settings.MEDIA_ROOT / path, "rb"),
        as_attachment=True,
    )
