import http

import django.test
from django.urls import reverse

__all__ = ["StaticURLTests"]


class StaticURLTests(django.test.TestCase):

    def test_about_url(self):
        response = django.test.Client().get(reverse("about:description"))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, "О проекте")
