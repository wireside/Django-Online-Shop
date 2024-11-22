import django.utils.timezone
import pytz

import users.models

__all__ = []


def birthday_context_processor(request):
    timezone_user = request.COOKIES.get("timezone")
    timezone_server = django.utils.timezone.now()

    if timezone_user:

        try:
            date_now = timezone_server.astimezone(pytz.timezone(timezone_user))
        except Exception:
            date_now = timezone_server
    else:
        date_now = timezone_server

    today = date_now.date()

    birthday_users = users.models.User.objects.active().filter(
        profile__birthday__month=today.month,
        profile__birthday__day=today.day,
    )

    return {"birthdays": birthday_users}
