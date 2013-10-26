from django.template import Template

def list_users(request):
    return ""

def login_page(request):

    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            inta = 5
    else:
        tmp = Template('templates/index.html')
        tmp.render()

    return ""

def register_page(request):
    return ""

