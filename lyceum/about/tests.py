from django.test import TestCase
from django.urls import reverse


class HomepageURLTests(TestCase):

    def test_about_url(self):
        url = reverse("description")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "О проекте")
