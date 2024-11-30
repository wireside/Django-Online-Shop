import django.contrib.auth
import django.test

import cart.models

__all__ = ["ModelsTests"]

User = django.contrib.auth.get_user_model()


class ModelsTests(django.test.TestCase):
    def test_create_cart_for_new_user(self):
        carts_count = cart.models.Cart.objects.count()

        user = User.objects.create_user(
            username="test",
            password="testpassword101",
        )
        user.save()

        self.assertEqual(cart.models.Cart.objects.count(), carts_count + 1)
