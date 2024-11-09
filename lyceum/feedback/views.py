from django.shortcuts import redirect, render
import feedback.forms as forms


def feedback(request):
    form = forms.FeedbackForm(request.POST or None)
    if form.is_valid():
        # name = form.cleaned_data["name"]
        # text = form.cleaned_data["text"]
        # email = form.cleaned_data["email"]
        return redirect("feedback:feedback")

    context = {"form": form}
    return render(request, "feedback/feedback.html", context)
