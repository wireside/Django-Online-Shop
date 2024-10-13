from django.http import HttpResponse

# Create your views here.
def index(request, pk):
    return HttpResponse("<body>Hello World</body>")