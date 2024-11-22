import django.contrib.auth.middleware

import users.models

__all__ = ["ProxyUserMiddleware"]


class ProxyUserMiddleware(
    django.contrib.auth.middleware.AuthenticationMiddleware,
):
    def process_request(self, request):
        super().process_request(request)
        if hasattr(request, "user") and request.user.is_authenticated:
            request.user = users.models.User.objects.get(id=request.user.id)
