from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput, ModelForm
from .models import My_crcard, My_buyes


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-input formEl"})),
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-input formEl"})),
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': "form-input formEl"})),
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': "form-input formEl"})),

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-input formEl"})),
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-input formEl"}))

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'email')


class CardForm(ModelForm):
    class Meta:
        model = My_crcard
        fields = ['numb', 'srok', 'three']
        widgets = {
            'numb': TextInput(attrs={
                'class': 'form-control formEl change',
                'placeholder': 'Номер карты',
            }),
            'srok': TextInput(attrs={
                'class': 'form-control formEl change',
                'placeholder': 'mm/yy',
            }),
            'three': TextInput(attrs={
                'class': 'form-control formEl change',
                'placeholder': 'CVV',
            }),}


class BuyForm(ModelForm):
    class Meta:
        model = My_buyes
        fields = ['adress', 'card']
        widgets = {
            'adress': TextInput(attrs={
                'placeholder': 'Адрес доставки',
                'class': 'form-control formEl change',
                'value': ""
            }),
            'card': TextInput(attrs={
                'class': 'form-control formEl change',
            }),}