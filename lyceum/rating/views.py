import django.shortcuts
import django.urls
import django.views.generic

import rating.models

__all__ = []


class DeleteView(django.views.generic.DeleteView):
    model = rating.models.Rating

    def get(self, *args, **kwargs):
        item_id = self.kwargs["pk"]
        rating.models.Rating.objects.filter(
            user=self.request.user,
            item_id=item_id,
        ).delete()

        return django.shortcuts.redirect(
            django.urls.reverse("catalog:item_detail", args=[item_id]),
        )
