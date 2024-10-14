from django.test import Client, TestCase


class StaticURLTests(TestCase):

    def test_item_list_url(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список элементов")

    def test_item_detail_url(self):
        response = Client().get("/catalog/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подробно элемент")

    def test_positive_converter(self):
        response = Client().get("/catalog/converter/001056/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1056")

    def test_customer_converter(self):
        response = Client().get("/catalog/re/0022301/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "0022301")
