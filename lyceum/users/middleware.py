import django.contrib.auth.middleware

import users.models


class UserMiddleware(django.contrib.auth.middleware.AuthenticationMiddleware):
    def process_request(self, request):
        super().process_request(request)
        if request.user.is_authenticated:
            request.user = users.models.User.objects.get(pk=request.user.id)
