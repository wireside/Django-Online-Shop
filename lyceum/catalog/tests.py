from django.test import TestCase
from django.urls import reverse


class CatalogURLTests(TestCase):

    def test_item_list_url(self):
        url = reverse("item_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список элементов")

    def test_item_detail_url(self):
        url = reverse("item_detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подробно элемент")
