import django.core.exceptions
import django.test
import parameterized

import catalog.models


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
    def setUp(self):
        self.category = catalog.models.Category.objects.create(
            name="Test category",
            slug="test-category",
        )
        self.tag = catalog.models.Tag.objects.create(
            name="Test tag",
            slug="test-tag",
        )

        super(ModelsTests, self).setUp()

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        catalog.models.Category.objects.all().delete()

        super(ModelsTests, self).tearDown()

    @parameterized.parameterized.expand(
        [
            ("Превосходно",),
            ("роскошно",),
            ("роскошно!",),
            ("роскошно@",),
            ("!роскошно",),
            ("не роскошно",),
        ]
    )
    def test_item_validator(self, text):
        items_count = catalog.models.Item.objects.count()

        item = catalog.models.Item(
            name="Тестовый товар",
            text=text,
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(
            catalog.models.Item.objects.count(),
            items_count + 1,
        )

    @parameterized.parameterized.expand(
        [
            ("Прев!осходно",),
            ("роскошный",),
            ("роскошное!",),
            ("оскошно@",),
            ("!р оскошно",),
            ("qwertyроскошно",),
        ]
    )
    def test_item_negative_validator(self, text):
        items_count = catalog.models.Item.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            item = catalog.models.Item(
                name="Тестовый товар",
                text=text,
                category=self.category,
            )
            item.full_clean()
            item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            items_count,
        )

    @parameterized.parameterized.expand(
        [
            (-100,),
            (0,),
            (64000,),
        ]
    )
    def test_category_negative_validator(self, weight):
        categories_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            test_category = catalog.models.Category(
                name="Тестовая категория",
                weight=weight,
                slug="test-cat",
            )
            test_category.full_clean()
            test_category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            categories_count,
        )

    @parameterized.parameterized.expand(
        [
            (1,),
            (100,),
            (32000,),
        ]
    )
    def test_category_validator(self, weight):
        categories_count = catalog.models.Category.objects.count()

        test_category = catalog.models.Category(
            name="Тестовая категория",
            weight=weight,
            slug=f"test-category{weight}",
        )
        test_category.full_clean()
        test_category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            categories_count + 1,
        )
