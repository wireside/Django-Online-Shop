import http

import django.test


class StaticURLTests(django.test.TestCase):

    def test_about_url(self):
        response = django.test.Client().get("/about/")
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, "О проекте")
