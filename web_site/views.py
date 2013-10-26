from django.shortcuts import get_object_or_404, render, redirect
from web_site.models import Pair


def list_pairs(request, template="pairs.html"):
    context = {"rooms": Pair.objects.all()}
    return render(request, template, context)


def pair(request, id, template="pair.html"):
    context = {"pair": get_object_or_404(Pair, id=id)}
    return render(request, template, context)


def create_pair(request):
    name = request.POST.get("name")
    lang = request.POST.get('lang')
    task = request.POST.get('task')
    uid = request.session.get('user_id')

    if name and lang and task and uid:
        pair_obj, created = Pair.objects.create(name=name, lang=lang, task=task, left_user_id=uid)
        return redirect(pair_obj)

    return redirect(list_pairs)

