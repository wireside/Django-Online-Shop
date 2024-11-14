import http

import django.core.exceptions
import django.test
from django.urls import reverse
import parameterized

import catalog.models

__all__ = [
    "CatalogItemsTests",
    "DetailItemTests",
    "ModelsTests",
    "StaticURLTests",
]


class StaticURLTests(django.test.TestCase):

    def test_item_list_url(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)


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


class CatalogItemsTests(django.test.TestCase):
    fixtures = ["fixtures/data.json"]

    def test_items_in_context(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_items_size(self):
        items_count = catalog.models.Item.objects.published().count()
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertEqual(len(response.context["items"]), items_count)

    def test_items_type(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertTrue(
            all(
                isinstance(
                    item,
                    catalog.models.Item,
                )
                for item in response.context["items"]
            ),
        )

    def test_categories_in_context(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertIn("categories", response.context)

    def test_categories_size(self):
        categories_count = (
            catalog.models.Category.objects.filter(
                is_published=True,
            )
            .exclude(
                items__exact=None,
            )
            .count()
        )
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertEqual(len(response.context["categories"]), categories_count)

    def test_categories_type(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertTrue(
            all(
                isinstance(
                    category,
                    catalog.models.Category,
                )
                for category in response.context["categories"]
            ),
        )


class DetailItemTests(django.test.TestCase):
    fixtures = ["fixtures/data.json"]

    @parameterized.parameterized.expand(
        [
            id
            for id in catalog.models.Item.objects.published().values_list(
                "id",
                flat=True,
            )
        ],
    )
    def test_item_in_context(self, item_id):
        response = django.test.Client().get(
            reverse(
                viewname="catalog:item_detail",
                args=[item_id],
            ),
        )
        self.assertIn("item", response.context)

    @parameterized.parameterized.expand(
        [
            id
            for id in catalog.models.Item.objects.published().values_list(
                "id",
                flat=True,
            )
        ],
    )
    def test_item_type(self, item_id):
        response = django.test.Client().get(
            reverse(
                viewname="catalog:item_detail",
                args=[item_id],
            ),
        )
        self.assertIsInstance(
            response.context["item"],
            catalog.models.Item,
        )
