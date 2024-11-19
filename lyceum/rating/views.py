import django.shortcuts
import django.urls

import rating.models


def delete(request, pk):
    rating.models.Rating.objects.filter(
        item_id=pk,
        user=request.user,
    ).delete()

    return django.shortcuts.redirect(
        django.urls.reverse("catalog:item_detail", args=[pk])
    )
