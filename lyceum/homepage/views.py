from django.http import HttpResponse


# Create your views here.
def index(response, pk):
    return HttpResponse("<body>Hello!</body>")
