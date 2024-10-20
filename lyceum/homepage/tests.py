import http

import django.test


class StaticURLTests(django.test.TestCase):

    def test_home_url(self):
        response = django.test.Client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Главная")

    def test_coffee_endpoint_status(self):
        response = django.test.Client().get("/coffee")
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)

    def test_coffee_endpoint_content(self):
        response = django.test.Client().get("/coffee")
        self.assertEqual(response.content, "Я чайник".encode())
