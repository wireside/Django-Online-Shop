import django.core.exceptions
import django.test
import parameterized

import catalog.models


class StaticURLTests(django.test.TestCase):

    def test_item_list_url(self):
        response = django.test.Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список элементов")

    @parameterized.parameterized.expand(
        [
            (100,),
            (0,),
            (64000,),
        ],
    )
    def test_item_detail_url(self, item_id):
        response = django.test.Client().get(f"/catalog/{item_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подробно элемент")

    @parameterized.parameterized.expand(
        [
            (-100,),
            (-1,),
            (-3125,),
        ],
    )
    def test_item_detail_invalid_id_url(self, item_id):
        response = django.test.Client().get(f"/catalog/{item_id}/")
        self.assertEqual(response.status_code, 404)

    @parameterized.parameterized.expand(
        [
            ("001056",),
            ("310031",),
            ("064000",),
        ],
    )
    def test_positive_converter(self, item_id):
        response = django.test.Client().get(f"/catalog/converter/{item_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item_id.lstrip("0"))

    @parameterized.parameterized.expand(
        [
            ("-001056",),
            ("-310031",),
            ("-064000",),
        ],
    )
    def test_positive_converter_negative_number(self, item_id):
        response = django.test.Client().get(f"/catalog/converter/{item_id}/")
        self.assertEqual(response.status_code, 404)

    @parameterized.parameterized.expand(
        [
            ("013e24PI*531",),
            ("f(x)'=lim(x->0)a",),
            ("O64O00",),
        ],
    )
    def test_positive_converter_invalid_number(self, item_id):
        response = django.test.Client().get(f"/catalog/converter/{item_id}/")
        self.assertEqual(response.status_code, 404)

    @parameterized.parameterized.expand(
        [
            ("001056",),
            ("310031",),
            ("064000",),
        ],
    )
    def test_customer_converter(self, item_id):
        response = django.test.Client().get(f"/catalog/re/{item_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item_id)

    @parameterized.parameterized.expand(
        [
            ("-001",),
            ("-310031",),
            ("-064000",),
        ],
    )
    def test_customer_converter_negative_number(self, item_id):
        response = django.test.Client().get(f"/catalog/re/{item_id}/")
        self.assertEqual(response.status_code, 404)

    @parameterized.parameterized.expand(
        [
            ("2PI + 2PIk",),
            ("3nO031",),
            ("one",),
        ],
    )
    def test_customer_converter_invalid_number(self, item_id):
        response = django.test.Client().get(f"/catalog/re/{item_id}/")
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
        ],
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
        ],
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
        ],
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
        ],
    )
    def test_category_validator(self, weight):
        categories_count = catalog.models.Category.objects.count()

        test_category = catalog.models.Category(
            name="Тестовая",
            weight=weight,
            slug=f"test-category{weight}",
        )
        test_category.full_clean()
        test_category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            categories_count + 1,
        )

    def test_canonical_category_name_negative(self):
        categories_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            test_category_1 = catalog.models.Category(
                name="одинаковое имя",
                slug="qwerty1235cat",
                weight=100,
            )
            test_category_1.full_clean()
            test_category_1.save()

            test_category_2 = catalog.models.Category(
                name="Одинаковое имя",
                slug="983507test-cat",
                weight=100,
            )
            test_category_2.full_clean()
            test_category_2.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            categories_count + 1,
        )

    def test_canonical_tag_name_negative(self):
        tags_count = catalog.models.Tag.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            test_tag_1 = catalog.models.Tag(
                name="одинаковое имя",
                slug="qwerty1235tagg111tag",
            )

            test_tag_2 = catalog.models.Tag(
                name="oдинAковое имя",
                slug="983507test-tagggg",
            )

            test_tag_1.full_clean()
            test_tag_1.save()

            test_tag_2.full_clean()
            test_tag_2.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tags_count + 1,
        )
