import pathlib
import tempfile

import django.conf
import django.core.files.base
import django.test
import django.urls

import feedback.forms
import feedback.models

__all__ = ["FeedbackFormTest"]


class FeedbackFormTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()
        cls.files_form = feedback.forms.FeedbackFileForm()
        cls.author_form = feedback.forms.FeedbackAuthorForm()

    def test_feedback_show_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        self.assertIn("feedback_form", response.context)
        self.assertIn("feedback_author", response.context)
        self.assertIn("file_form", response.context)

    def test_name_label(self):
        name_label = FeedbackFormTest.author_form.fields["name"].label
        self.assertEqual(name_label, "Имя")

    def test_text_label(self):
        text_label = FeedbackFormTest.form.fields["text"].label
        self.assertEqual(text_label, "Сообщение")

    def test_mail_label(self):
        mail_label = FeedbackFormTest.author_form.fields["mail"].label
        self.assertEqual(mail_label, "Электронная почта")

    def test_name_help_text(self):
        name_help_text = FeedbackFormTest.author_form.fields["name"].help_text
        self.assertEqual(
            name_help_text,
            "Введите ваше имя",
        )

    def test_text_help_text(self):
        text_help_text = FeedbackFormTest.form.fields["text"].help_text
        self.assertEqual(
            text_help_text,
            "Введите текст сообщения",
        )

    def test_mail_help_text(self):
        mail_help_text = FeedbackFormTest.author_form.fields["mail"].help_text
        self.assertEqual(mail_help_text, "mail@example.com")

    def test_unable_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Тестовое имя",
            "text": "Тестовый текст",
            "mail": "notmail",
        }

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertTrue(response.context["form"].has_error("mail"))
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count,
        )

    def test_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Тестовое имя",
            "text": "Тестовый текст",
            "mail": "existing@mail.com",
        }

        self.assertFalse(
            feedback.models.Feedback.objects.filter(
                text="Тестовый текст",
            ).exists(),
        )
        self.assertFalse(
            feedback.models.FeedbackAuthor.objects.filter(
                name="Тестовое имя",
                mail="existing@mail.com",
            ).exists(),
        )

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count + 1,
        )

        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                text="Тестовый текст",
            ).exists(),
        )
        self.assertTrue(
            feedback.models.FeedbackAuthor.objects.filter(
                name="Тестовое имя",
                mail="existing@mail.com",
            ).exists(),
        )

    @django.test.override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory().name,
    )
    def test_file_upload(self):
        files = [
            django.core.files.base.ContentFile(
                f"file_{index}".encode(),
                name="filename",
            )
            for index in range(10)
        ]
        form_data = {
            "name": "Тестовое имя",
            "text": "test text",
            "mail": "existing@mail.com",
            "file": files,
        }
        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        feedback_item = feedback.models.Feedback.objects.get(text="test text")
        self.assertEqual(feedback_item.files.count(), 10)
        feedback_files = feedback_item.files.all()

        media_root = pathlib.Path(django.conf.settings.MEDIA_ROOT)

        for index, file in enumerate(feedback_files):
            uploaded_file = media_root / file.file.path
            self.assertEqual(
                uploaded_file.open().read(),
                f"file_{index}",
            )
