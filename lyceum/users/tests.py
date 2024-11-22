import datetime
import unittest.mock

import django.test
import django.urls
import django.utils.timezone
import pytz

import users.context_processors
import users.models

__all__ = []


class TestContextProcessorBirthday(django.test.TestCase):
    def setUp(self):
        self.factory = django.test.RequestFactory()

        today = django.utils.timezone.now().date()
        tomorrow = today + datetime.timedelta(days=1)

        self.user_today = users.models.User.objects.create(
            username="today_user",
            email="today@example.com",
        )
        users.models.Profile.objects.create(
            user=self.user_today,
            birthday=today,
        )

        self.user_tomorrow = users.models.User.objects.create(
            username="tomorrow_user",
            email="tomorrow@example.com",
        )
        users.models.Profile.objects.create(
            user=self.user_tomorrow,
            birthday=tomorrow,
        )

    def test_birthdays_in_context(self):
        request = self.factory.get("/")
        context = users.context_processors.birthday_context_processor(request)
        self.assertIn("birthdays", context)

    def test_correct_answer_today_users(self):
        request = self.factory.get("/")
        context = users.context_processors.birthday_context_processor(request)

        users_birthday = context["birthdays"]

        self.assertEqual(len(users_birthday), 1)
        self.assertEqual(users_birthday[0].username, "today_user")

    @unittest.mock.patch("django.utils.timezone.now")
    def test_no_birthday_users(self, mock_now):
        mock_now.return_value = pytz.UTC.localize(
            django.utils.timezone.datetime.now()
            + datetime.timedelta(
                days=5,
            ),
        )
        request = self.factory.get("/")
        context = users.context_processors.birthday_context_processor(request)
        birthday_users = context["birthdays"]

        self.assertEqual(len(birthday_users), 0)


class TestUsersActivation(django.test.TestCase):
    def setUp(self):
        django.test.Client().post(
            django.urls.reverse("users:signup"),
            {
                "username": "user",
                "email": "user@user.com",
                "password1": "Q12W3er$",
                "password2": "Q12W3er$",
            },
            follow=True,
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_activate_user(self):

        user = users.models.User.objects.get(username="user")

        self.assertFalse(user.is_active)

        django.test.Client().get(
            django.urls.reverse("users:activate", args=[user.pk]),
            follow=True,
        )

        user = users.models.User.objects.get(username="user")
        self.assertTrue(user.is_active)
