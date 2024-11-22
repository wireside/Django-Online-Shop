import django.conf
import django.http
import django.views

__all__ = []


class FileDownloadView(django.views.View):
    def get(self, request, path, *args, **kwargs):
        return django.http.FileResponse(
            open(django.conf.settings.MEDIA_ROOT / path, "rb"),
            as_attachment=True,
        )
