from django.shortcuts import render, redirect
from web_site.models import Pair
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def login(request, template="login.html"):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None and user.is_active:
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
    if request.user.is_authenticated():
        context = {"pairs": Pair.objects.all()}
        return render(request, template, context)
    else:
        return redirect(login)


@login_required
def pair(request, pair_id, template="pair.html"):
    user_id = request.session.get("user_id")
    pair_obj = Pair.objects.get(id=pair_id)
    if pair_obj is None:
        return redirect(lobby)

    if pair_obj.is_user_in(user_id):
        request.session['pair_id'] = pair_obj.id
        return render(request, template, pair_obj.get_context())

    if not pair_obj.has_free_spot():
        return redirect(lobby)

    pair_obj.push_user(request.user)
    request.session['pair_id'] = pair_obj.id

    return render(request, template, pair_obj.get_context())


@login_required
def create_pair(request):
    name = request.POST.get("name")
    lang = request.POST.get('lang')
    task = request.POST.get('task')

    if name and lang and task:
        pair_obj = Pair.objects.create(
            name=name,
            lang=lang,
            task=task,
            owner=request.user,
            turn=request.user
        )
        request.session['created_pair_id'] = pair_obj.id
        return redirect(pair_obj)

    return redirect(lobby)
