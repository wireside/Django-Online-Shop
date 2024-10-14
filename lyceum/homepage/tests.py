from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):

    def test_home_url(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Главная")

    def test_coffee_endpoint_status(self):
        response = Client().get("/coffee")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_endpoint_content(self):
        response = Client().get("/coffee")
        self.assertEqual(response.content, "Я чайник".encode())
