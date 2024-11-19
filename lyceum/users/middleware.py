import django.contrib.auth.middleware

import users.models

__all__ = ["UserMiddleware"]


class UserMiddleware(django.contrib.auth.middleware.AuthenticationMiddleware):
    def process_request(self, request):
        super().process_request(request)
        if hasattr(request, "user") and request.user.is_authenticated:
            request.user.__class__ = users.models.User
