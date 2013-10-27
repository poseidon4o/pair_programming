from django.shortcuts import get_object_or_404, render, redirect
from web_site.models import Pair
from pprint import pprint


def lobby(request, template="lobby.html"):
    context = {"pairs": Pair.objects.all()}
    return render(request, template, context)


def pair(request, id, template="pair.html"):
    context = {"pair": get_object_or_404(Pair, id=id)}
    return render(request, template, context)


def create_pair(request):
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

