from django.shortcuts import get_object_or_404, render, redirect
from web_site.models import Pair
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def login(request, template="login.html"):
    if request.method == "POST":
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            request.session["username"] = user.id
            return redirect(lobby)
    else:
        return render(request, template)
    return render(request, template)

def logout(request):
    try:
        del request.session["username"]

    except KeyError:
        pass
    return redirect(login)
def register(request, template="register.html"):
    if request.method == "POST":
        if request.POST.get("password") == request.POST.get("password_again"):
            User.objects.create_user(request.POST.get("username"), request.POST.get("email"), request.POST.get("password"))
            return redirect(login)
    else:
        return render(request, template)
    return render(register)

def lobby(request, template="lobby.html"):
    if request.session.get("username"):
        context = {"pairs": Pair.objects.all()}
        return render(request, template, context)
    else:
        return redirect(login)

def pair(request, id, template="pair.html"):
    if request.session.get("username"):
        context = {"pair": get_object_or_404(Pair, id=id)}
        #TODO: give ID
        return render(request, template, context)
    else:
        return redirect(login)

def create_pair(request):
    if request.session.get("username"):
        name = request.POST.get("name")
        lang = request.POST.get('lang')
        task = request.POST.get('task')
        uid = request.session.get('user_id')

        if name and lang and task:  # and uid
            pair, created = Pair.objects.create(name=name, lang=lang, task=task, l_u_id=uid), True
            print("pair created, redirect to pair page")
            return redirect(pair)

        pprint(request.session)
        print(vars(request.session))
        return redirect(lobby)
    else:
        return redirect(login)
