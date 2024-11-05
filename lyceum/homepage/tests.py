import http

import django.test
from django.urls import reverse
import catalog.models


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


class HomepageItemsTests(django.test.TestCase):
    fixtures = ["fixtures/data.json"]

    def test_items_in_context(self):
        response = django.test.Client().get(reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_items_size(self):
        items_count = catalog.models.Item.objects.on_main().count()
        response = django.test.Client().get(reverse("homepage:home"))
        self.assertEqual(len(response.context["items"]), items_count)

    def test_items_type(self):
        response = django.test.Client().get(reverse("homepage:home"))
        self.assertTrue(
            all(
                isinstance(
                    item,
                    catalog.models.Item,
                )
                for item in response.context["items"]
            ),
        )
