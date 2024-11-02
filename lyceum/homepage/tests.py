import http

import django.test
from django.urls import reverse


class StaticURLTests(django.test.TestCase):

    def test_home_url(self):
        response = django.test.Client().get(reverse("homepage:home"))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, "Главная")

    def test_coffee_endpoint_status(self):
        response = django.test.Client().get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)

    def test_coffee_endpoint_content(self):
        response = django.test.Client().get(reverse("homepage:coffee"))
        self.assertEqual(response.content, "Я чайник".encode())


class ContextTests(django.test.TestCase):
    def test_homepage_context(self):
        response = self.client.get(reverse("homepage:home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.context)
