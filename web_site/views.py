from django.shortcuts import get_object_or_404, render, redirect
from web_site.models import Pair
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def login(request, template="login.html"):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None and user.is_active :
            auth.login(request, user)
            request.session["user_id"] = user.id
            return redirect(lobby)
    else:
        return render(request, template)
    return render(request, template)


def logout(request):
    try:
        auth.logout(request)
        del request.session["user_id"]
    except KeyError:
        pass

    return redirect(login)


def register(request, template="register.html"):
    if request.method == "POST":
        if request.POST.get("password") == request.POST.get("password_again"):
            User.objects.create_user(
                request.POST.get("username"),
                request.POST.get("email"),
                request.POST.get("password")
            )
            return redirect(login)
    else:
        return render(request, template)
    return render(register)


@login_required
def lobby(request, template="lobby.html"):
    if request.user.is_authenticated() :
        context = {"pairs": Pair.objects.all()}
        return render(request, template, context)
    else:
        return redirect(login)


@login_required
def pair(request, id, template="pair.html"):
    user_id = request.session.get("user_id")
    if user_id is not None:
        p_obj = get_object_or_404(Pair, id=id)
        p_obj.l_u_id = user_id
        context = {
            "pair": p_obj,
            'user_id': user_id,
            'pair_owner': p_obj.l_u_id
        }
        return render(request, template, context)
    redirect(login)


@login_required
def create_pair(request):
    name = request.POST.get("name")
    lang = request.POST.get('lang')
    task = request.POST.get('task')
    uid = request.session.get('user_id')

    if name and lang and task:
        pair, created = Pair.objects.create(name=name, lang=lang, task=task, l_u_id=uid), True
        return redirect(pair)

    pprint(request.session)

    return redirect(lobby)
