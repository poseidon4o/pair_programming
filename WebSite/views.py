from django.template import Template
# Create your views here.
#from WebSite.models import UUser
from django.contrib.auth.models import User
from django.template.response import TemplateResponse

def list_users(request):
    return ""

def login_page(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            #TODO: some intersting shits :D
            return TemplateResponse(request, 'lobby.html')
    return TemplateResponse(request, 'index.html')

def register_page(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST and 'password_again' in request.POST:
            #u_data = User.validate(request.POST)
            u_data = {'username': 1, 'password': 2}
            if u_data is not None:
                user = User.create_user(u_data['username'], u_data['password'])
                # TODO: add user to session
                return TemplateResponse(request, 'lobby.html')
    return TemplateResponse(request, 'register.html')
