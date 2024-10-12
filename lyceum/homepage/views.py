from django.http import HttpResponse


# Create your views here.
def home(response):
    return HttpResponse("<body>Главная</body>")
