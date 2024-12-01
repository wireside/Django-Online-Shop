import django.contrib.auth
import django.test

import cart.models
import users.models

__all__ = ["ModelsTests"]


class ModelsTests(django.test.TestCase):
    def test_create_cart_for_new_user(self):
        carts_count = cart.models.Cart.objects.count()

        user = users.models.User.objects.create_user(
            username="test",
            password="testpassword101",
        )
        user.save()

        self.assertEqual(cart.models.Cart.objects.count(), carts_count + 1)
