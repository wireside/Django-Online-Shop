import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.views.generic

import feedback.forms
import feedback.models

__all__ = []


class IndexView(django.views.generic.FormView):
    template_name = "feedback/feedback.html"

    def get(self, request, *args, **kwargs):
        context = {
            "feedback_author": feedback.forms.FeedbackAuthorForm(),
            "feedback_form": feedback.forms.FeedbackForm(),
            "file_form": feedback.forms.FeedbackFileForm(),
        }
        return django.shortcuts.render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        feedback_author = feedback.forms.FeedbackAuthorForm(request.POST)
        feedback_form = feedback.forms.FeedbackForm(request.POST)
        file_form = feedback.forms.FeedbackFileForm(request.POST)

        forms = (feedback_author, feedback_form, file_form)

        if all(form.is_valid() for form in forms):
            django.core.mail.send_mail(
                subject=f"Привет {feedback_author.cleaned_data['name']}",
                message=feedback_form.cleaned_data["text"],
                from_email=django.conf.settings.MAIL,
                recipient_list=[feedback_author.cleaned_data["mail"]],
                fail_silently=True,
            )

            feedback_item = feedback.models.Feedback.objects.create(
                **feedback_form.cleaned_data,
            )

            feedback.models.FeedbackAuthor.objects.create(
                feedback=feedback_item,
                **feedback_author.cleaned_data,
            )

            for file in request.FILES.getlist("file"):
                feedback.models.FeedbackFile.objects.create(
                    file=file,
                    feedback=feedback_item,
                )

            django.contrib.messages.success(
                request,
                "Фидбек отправлен, спасибо!",
            )

            return django.shortcuts.redirect(
                django.shortcuts.reverse("feedback:feedback"),
            )

        context = {
            "feedback_author": feedback_author,
            "feedback_form": feedback_form,
            "file_form": file_form,
        }

        return django.shortcuts.render(request, self.template_name, context)
