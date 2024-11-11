import django.contrib.admin

import feedback.models


class FeedbackAuthor(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackAuthor
    fields = (
        feedback.models.FeedbackAuthor.name.field.name,
        feedback.models.FeedbackAuthor.mail.field.name,
    )
    can_delete = False


class FeedbackFiles(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackFile
    fields = (feedback.models.FeedbackFile.file.field.name,)


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.status.field.name,
    )
    inlines = (
        FeedbackAuthor,
        FeedbackFiles,
    )
