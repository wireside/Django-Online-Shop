import django.core.exceptions
import django.test

from catalog import models


class StaticURLTests(django.test.TestCase):

    def test_item_list_url(self):
        response = django.test.Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список элементов")

    def test_item_detail_url(self):
        response = django.test.Client().get("/catalog/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подробно элемент")

    def test_item_detail_invalid_id_url(self):
        response = django.test.Client().get("/catalog/-123/")
        self.assertEqual(response.status_code, 404)

    def test_positive_converter(self):
        response = django.test.Client().get("/catalog/converter/001056/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1056")

    def test_positive_converter_negative_number(self):
        response = django.test.Client().get("/catalog/converter/-01324531/")
        self.assertEqual(response.status_code, 404)

    def test_positive_converter_invalid_number(self):
        response = django.test.Client().get("/catalog/converter/013e24PI*531/")
        self.assertEqual(response.status_code, 404)

    def test_customer_converter(self):
        response = django.test.Client().get("/catalog/re/0022301/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "0022301")

    def test_customer_converter_negative_number(self):
        response = django.test.Client().get("/catalog/re/-301/")
        self.assertEqual(response.status_code, 404)

    def test_customer_converter_invalid_number(self):
        response = django.test.Client().get("/catalog/re/30oneTwoOne_one1/")
        self.assertEqual(response.status_code, 404)


class ModelsTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = models.Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test-category-slug",
            weight=100,
        )
        cls.tag = models.Tag.objects.create(
            is_published=True,
            name="Тествовый тег",
            slug="test-tag-slug",
        )

    def test_custom_validator_create_without_needed_words(self):
        item_count = models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = models.Item(
                name="Тестовый товар",
                category=self.category,
                text="Тестовое описание",
            )
            self.item.full_clean()
            self.item.tags.add(ModelsTests.tag)
            self.item.save()

        self.assertEqual(
            models.Item.objects.count(),
            item_count,
        )

    def test_custom_validator_create_with_needed_words(self):
        item_count = models.Item.objects.count()
        self.item = models.Item(
            name="Тестовый товар",
            category=self.category,
            text="тестовое превосходно описание",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelsTests.tag)

        self.assertEqual(
            models.Item.objects.count(),
            item_count + 1,
        )
