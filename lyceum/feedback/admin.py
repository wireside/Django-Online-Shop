import django.contrib.admin

import feedback.models

__all__ = ["FeedbackAdmin", "FeedbackAuthor", "FeedbackFiles"]


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


@django.contrib.admin.register(feedback.models.StatusLog)
class StatusLogAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to_status.field.name,
    )


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

    def save_model(self, request, obj, form, change):
        if change:
            queryset = feedback.models.Feedback.objects.get(id=obj.id)
            old_status = queryset.status
            if old_status != obj.status:
                feedback.models.StatusLog.objects.create(
                    feedback=obj,
                    user=request.user,
                    from_status=old_status,
                    to_status=obj.status,
                )

            obj.save()

        super().save_model(request, obj, form, change)
