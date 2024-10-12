import unittest
from django.test import Client
from django.urls import reverse


class HomepageURLTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()

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


if __name__ == "__main__":
    unittest.main()
