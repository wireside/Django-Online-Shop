from django.test import TestCase
from django.urls import reverse


class HomepageURLTests(TestCase):

    def test_home_url(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Главная")
