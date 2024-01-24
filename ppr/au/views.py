from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import RegisterUserForm, CustomUserChangeForm, CardForm, BuyForm
from main.models import Thing
import re
from .models import User, My_crcard


@login_required
def prof_v(request):
    tovar_c = request.user.tovars_c.all()
    tovar_b = request.user.my_buyes_set.order_by('-dateBuy')
    cards = request.user.my_crcard_set.all()
    User = get_user_model()
    users = User.objects.all()
    return render(request, "au/prof_w.html", {'tovar_c': tovar_c, 'tovar_b': tovar_b, 'users': users, 'cards': cards})


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'au/register.html'
    success_url = reverse_lazy('prof')


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваш аккаунт создан!')
            return redirect('prof')
        else:
            return render(request, 'au/register.html', {'form': form})
    else:
        form = RegisterUserForm()
    return render(request, 'au/register.html', {'form': form})


def сhangeUserData(request, pk):
    data = {}
    User = get_user_model()
    current_user = User.objects.get(id = pk)
    data['currentUsername'] = current_user.username
    data['currentEmail'] = current_user.email
    data['usernameError'] = ""
    data['emailError'] = ""

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST)

        IsOk = True
        data['currentUsername'] = request.POST.get('username')
        data['currentEmail'] = request.POST.get('email')
        if User.objects.filter(username=request.POST.get('username')).exists():
            if current_user != User.objects.get(username=request.POST.get('username')):
                IsOk = False
                data['usernameError'] = "Данный логин занят"
        if User.objects.filter(email=request.POST.get('email')).exists():
            if current_user != User.objects.get(email=request.POST.get('email')):
                IsOk = False
                data['emailError'] = "Данный Email занят"

        if IsOk and form.is_valid():
            current_user.username = request.POST.get('username')
            current_user.email = request.POST.get('email')
            current_user.save()
            return redirect('prof')
    else:
        form = CustomUserChangeForm()
    data['form'] = form
    return render(request, 'au/change.html', data)


def addCard(request):
    error = {}
    form = CardForm()
    if request.method == 'POST':
        form = CardForm(request.POST)
        AllOk = True
        if form.is_valid():
            f = form.save(commit=False)
            if len(f.numb) != 16:
                error['num'] = 'Длина номера должна быть 16'
                AllOk = False
            elif not f.numb.isdigit():
                error['num'] = 'Номер должен состоять только из цифр'
                AllOk = False
            if re.match(r'\d\d/\d\d', f.srok) is None:
                error['sr'] = 'Данные должны иметь вид мм/гг'
                AllOk = False
            elif int(f.srok[:2]) not in range(1, 13):
                error['sr'] = 'Несуществующая дата'
                AllOk = False
            if len(f.three) != 3:
                error['th'] = 'Длина CVV должна быть 3'
                AllOk = False
            elif not f.three.isdigit():
                error['th'] = 'CVV должен состоять только из цифр'
                AllOk = False
            if AllOk:
                f.owner = request.user
                f.save()
                return redirect('prof')


    data = {
        'form': form,
        'error': error
    }
    return render(request, 'au/addCard.html', data)

class UpCrCard(UpdateView):
    model = My_crcard
    template_name = 'au/addCard.html'
    context_object_name = 'el'
    form_class = CardForm
    success_url = reverse_lazy("prof")

def buyTov(request, pk):
    error = ''
    form = BuyForm()
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.tov = Thing.objects.get(id=pk)
            f.buyer = request.user
            f.save()
            curent_tovar = Thing.objects.get(id=pk)
            request.user.tovars_c.remove(curent_tovar)
            return redirect('prof')

    cards = request.user.my_crcard_set.all()
    error = form.errors
    data = {
        'form': form,
        'cards': cards,
        'error': error
    }
    return render(request, 'au/Buy.html', data)

def delCrCard(request, pk):
    current_card = My_crcard.objects.get(id=pk)
    current_card.delete()
    return prof_v(request)

def MyDeleteUs(request, pk):
    User = get_user_model()
    User.objects.get(id=pk).delete()
    return prof_v(request)
