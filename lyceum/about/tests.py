import django.test


class StaticURLTests(django.test.TestCase):

    def test_about_url(self):
        response = django.test.Client().get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "О проекте")
