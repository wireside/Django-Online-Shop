import re

from django.conf import settings

__all__ = []

counter = 1


class ReverseRussianMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global counter
        response = self.get_response(request)
        if settings.ALLOW_REVERSE and counter % 10 == 0:
            response.content = self.reverse_only_russian_words(
                response.content.decode(),
            ).encode()

        counter += 1
        return response

    def reverse_only_russian_words(self, content):
        return re.sub(r"\b[А-яёЁ]+\b", lambda m: m.group()[::-1], content)
