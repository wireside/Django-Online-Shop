import unittest
from django.test import Client
from django.urls import reverse


class HomepageURLTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_url(self):
        url = reverse("about")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "О проекте")


if __name__ == "__main__":
    unittest.main()
