import django.conf
import django.contrib
import django.core.mail
import django.shortcuts
import django.urls

import feedback.forms
import feedback.models


def index(request):
    feedback_author = feedback.forms.FeedbackAuthorForm(request.POST or None)
    feedback_form = feedback.forms.FeedbackForm(request.POST or None)
    file_form = feedback.forms.FeedbackFileForm(request.POST or None)
    context = {
        "feedback_author": feedback_author,
        "feedback_form": feedback_form,
        "file_form": file_form,
    }

    forms = (feedback_author, feedback_form, file_form)

    if request.method == "POST" and all(form.is_valid() for form in forms):
        django.core.mail.send_mail(
            subject=f"Привет {feedback_author.cleaned_data['name']}",
            message=f"{feedback_form.cleaned_data['text']}",
            from_email=django.conf.settings.MAIL,
            recipient_list=[feedback_author.cleaned_data["mail"]],
            fail_silently=True,
        )
        feedback_item = feedback.models.Feedback.objects.create(
            **feedback_form.cleaned_data,
        )
        feedback_item.save()
        feedback.models.FeedbackAuthor.objects.create(
            feedback=feedback_item,
            **feedback_author.cleaned_data,
        )
        for file in request.FILES.getlist(
            feedback.models.FeedbackFile.file.field.name,
        ):
            feedback.models.FeedbackFile.objects.create(
                file=file,
                feedback=feedback_item,
            )

        django.contrib.messages.success(
            request,
            "Фидбек отправлен, спасибо!",
        )
        return django.shortcuts.redirect(
            django.urls.reverse("feedback:feedback"),
        )

    return django.shortcuts.render(
        request=request,
        template_name="feedback/feedback.html",
        context=context,
    )
