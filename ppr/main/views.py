import traceback

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .models import Thing, Image
from .forms import ThingForm, ImageForm
from django.views.generic import DetailView, UpdateView, DeleteView
from au.models import My_card


def inf_home(request, MytypeData):
    if MytypeData:
        tovar = Thing.objects.filter(typeData=MytypeData).order_by('-date')
    else:
        tovar = Thing.objects.order_by('-date')

    form = {}
    if request.method == 'POST':
        if 'searchT' in request.POST:
            form["sort"] = request.POST.get("SortData")
            form["minim"] = request.POST.get("min")
            form["maxim"] = request.POST.get("max")
            form["search"] = request.POST.get("searchT")
            if form["sort"] == "2":
                tovar = tovar.order_by('date')
            if form["minim"].isdigit():
                if form["maxim"].isdigit():
                    pass
                    tovar = filter(lambda x: (x.cost < int(form["maxim"])) and (x.cost > int(form["minim"])), tovar)
                else:
                    form["maxim"] = ""
                    tovar = tuple(filter(lambda x: x.cost > int(form["minim"]), tovar))
            else:
                form["minim"] = ""
                if form["maxim"].isdigit():
                    tovar = tuple(filter(lambda x: x.cost < int(form["maxim"]), tovar))
                else:
                    form["maxim"] = ""
            if form["search"]:
                tovar = tuple(filter(lambda x: form["search"].lower() in x.title.lower(), tovar))
        # else:
        #     current_tov = Thing.objects.get(id = int(request.POST.get('basket')))
        #     user_tovar = My_card(buyer=request.user, tov=current_tov, amount=1)
        #     user_tovar.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            current_tov = Thing.objects.get(id=int(request.POST.get('basket')))
            user_tovar = My_card(buyer=request.user, tov=current_tov, amount=1)
            user_tovar.save()
            return JsonResponse({"ok": 'ok'})
    if request.user.is_authenticated:
        cur_tovars = request.user.tovars_c.all()
    else:
        cur_tovars = []

    if MytypeData == 'rider':
        tit = "Для наездника"
    elif MytypeData == 'stable':
        tit = "Для конюшни"
    elif MytypeData == 'horse':
        tit = "Для лошади"
    else:
        tit = "Каталог"
    return render(request, 'main/inf_home.html', {'tovar': tovar, 'title': tit, 'form': form, 'cur_tov': cur_tovars})


def myDinamic(request, pk):
    keyy = Thing.objects.get(id=pk)
    tovars = request.user.tovars_c.all()
    Fl = keyy in tovars
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        current_tov = Thing.objects.get(id=int(request.POST.get('basket')))
        user_tovar = My_card(buyer=request.user, tov=current_tov, amount=1)
        user_tovar.save()
        return JsonResponse({"ok": 'ok'})
    return render(request, 'main/detail.html', {'keyy': keyy, 'Fl': Fl})


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class MyUpdate(UpdateView):
    model = Thing
    template_name = 'main/create.html'
    context_object_name = 'keyy'
    form_class = ThingForm
    success_url = 'add_pic'

    def dispatch(self, request, *args, **kwargs):
        # Получаем значение id из параметров URL или из POST-запроса
        id = kwargs.get('pk') or request.POST.get('id')
        # Проверяем, существует ли товар с указанным id
        try:
            thing = Thing.objects.get(pk=id)
        except Thing.DoesNotExist:
            # Если товар не существует, перенаправляем пользователя на другую страницу
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class MyDelete(DeleteView):
    model = Thing
    success_url = '/'
    context_object_name = 'keyy'
    template_name = 'main/del.html'
    def dispatch(self, request, *args, **kwargs):
        # Получаем значение id из параметров URL или из POST-запроса
        id = kwargs.get('pk') or request.POST.get('id')
        # Проверяем, существует ли товар с указанным id
        try:
            thing = Thing.objects.get(pk=id)
        except Thing.DoesNotExist:
            # Если товар не существует, перенаправляем пользователя на другую страницу
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def create(request):
    form = ThingForm()
    if request.method == 'POST':
        form = ThingForm(request.POST)
        if form.is_valid():
            ind = form.save()
            return redirect('add_picture', ind.id)

    data = {
        'form': form,
    }
    return render(request, 'main/create.html', data)


def MyAddTovar(request, pk):
    curent_tovar = Thing.objects.filter(id=pk)
    if curent_tovar:
        user_tovar = My_card(buyer=request.user, tov=curent_tovar[0], amount=1)
        user_tovar.save()
        return redirect('dinamic', pk)
    else:
        return redirect('/')


def MyAddIm(request, pk):
    form = ImageForm()
    curent_tovar = Thing.objects.filter(id=pk)
    if curent_tovar:
        if request.method == 'POST':
            ImForm = ImageForm(request.POST, request.FILES)
            if ImForm.is_valid():
                im = ImForm.save(commit=False)
                im.tov = curent_tovar[0]
                im.save()
        imgs = curent_tovar[0].image_set.all()
        idTov = pk
        return render(request, 'main/add_picture.html', {'imgs': imgs, 'form': form, 'idT': idTov})
    else:
        return redirect('/')

def MyDeleteTovar(request, pk):
    curent_tovar = Thing.objects.filter(id=pk)
    if curent_tovar:
        request.user.tovars_c.remove(curent_tovar[0])
        return redirect('prof')
    else:
        return redirect('/')


def MyDelIm(request, pk):
    im = Image.objects.filter(id=pk)
    if im:
        curent_tovar = im[0].tov
        im[0].delete()
        return redirect('add_picture', pk=curent_tovar.id)
    else:
        return redirect('/')

