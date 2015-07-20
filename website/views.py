from django.views.generic import TemplateView


# Create your views here.
def contact(request):
    if request.method == 'POST':
        print('request from ', request.POST['email'])