import decimal
import http

import django.test
import django.urls
import parameterized

import cart.models
import catalog.models
import users.models

__all__ = ["ModelsTests"]


class SignalsTests(django.test.TestCase):
    def test_create_cart_for_new_user(self):
        carts_count = cart.models.Cart.objects.count()

        user = users.models.User.objects.create_user(
            username="test",
            password="testpassword101",
        )
        user.save()

        self.assertEqual(cart.models.Cart.objects.count(), carts_count + 1)


class StaticURLTests(django.test.TestCase):
    def setUp(self):
        self.user = users.models.User.objects.create_user(
            username="testuser",
            password="password123",
        )

    def test_redirect_unauthorized_user(self):
        response = django.test.Client().get(django.urls.reverse("cart:cart"))
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, django.urls.reverse("users:login"))

    def test_cart_url(self):
        self.client.login(username="testuser", password="password123")

        response = self.client.get(django.urls.reverse("cart:cart"))

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
        self.user = users.models.User.objects.create_user(
            username="test",
            password="testpassword101",
        )

        super(ModelsTests, self).setUp()

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        catalog.models.Category.objects.all().delete()
        users.models.User.objects.all().delete()

        super(ModelsTests, self).tearDown()

    def test_add_to_cart(self):
        cart_items_count = self.user.cart.items.count()
        item = catalog.models.Item.objects.create(
            name="item",
            text="Test item",
            category=self.category,
            price=1000,
        )
        item.save()

        cart_item = cart.models.CartItem.objects.create(
            cart=self.user.cart,
            item=item,
        )
        cart_item.save()

        self.assertEqual(self.user.cart.items.count(), cart_items_count + 1)

    @parameterized.parameterized.expand(
        [
            ("1256.87",),
            ("96500.5",),
            ("3500",),
        ],
    )
    def test_cart_total_price(self, decimal_price):
        cart_items_count = self.user.cart.items.count()
        quantity = 3
        price = decimal.Decimal(decimal_price)
        total_price = price * quantity

        item = catalog.models.Item.objects.create(
            name="item",
            text="Test item",
            category=self.category,
            price=price,
        )
        item.save()

        cart_item = cart.models.CartItem.objects.create(
            cart=self.user.cart,
            item=item,
            quantity=quantity,
        )
        cart_item.save()

        self.assertEqual(self.user.cart.items.count(), cart_items_count + 1)
        self.assertEqual(self.user.cart.get_total_price(), total_price)
