import http

import django.test
import django.urls

import catalog.models
import homepage.forms

__all__ = ["HomepageEchoTests", "HomepageItemsTests", "StaticURLTests"]


class StaticURLTests(django.test.TestCase):

    def test_home_url(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:home"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, "Главная")

    def test_coffee_endpoint_status(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:coffee"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.IM_A_TEAPOT)

    def test_coffee_endpoint_content(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:coffee"),
        )
        self.assertEqual(response.content, "Я чайник".encode())


class HomepageItemsTests(django.test.TestCase):
    fixtures = ["fixtures/data.json"]

    def test_items_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:home"),
        )
        self.assertIn("items", response.context)

    def test_items_size(self):
        items_count = catalog.models.Item.objects.on_main().count()
        response = django.test.Client().get(
            django.urls.reverse("homepage:home"),
        )
        self.assertEqual(len(response.context["items"]), items_count)

    def test_items_type(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:home"),
        )
        self.assertTrue(
            all(
                isinstance(
                    item,
                    catalog.models.Item,
                )
                for item in response.context["items"]
            ),
        )


class HomepageEchoTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = homepage.forms.EchoForm()

    def test_show_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:echo"),
        )
        self.assertIn("echo_form", response.context)

    def test_text_label(self):
        text_label = HomepageEchoTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст")

    def test_submit_form(self):
        form_data = {"text": "Тестовый текст"}

        response = django.test.Client().post(
            django.urls.reverse("homepage:echo_submit"),
            data=form_data,
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(
            "Тестовый текст".encode("utf-16"),
            response.content,
        )
