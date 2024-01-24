from django.db import models

from .models import Thing
from django.forms import ModelForm, TextInput, Textarea, RadioSelect
from .models import Image
from django import forms


class ThingForm(ModelForm):
    typeData = forms.ChoiceField(choices=(("rider", "Для наездника"), ("horse", "Для лошади"), ("stable", "Для конюшни")), widget=RadioSelect())
    class Meta:
        model = Thing
        fields = ['title', 'description', 'inform', 'typeData', 'cost']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'название товара',
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'краткое описание товара',
            }),
            'inform': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'описание товара',
            }),
            'cost': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'цена товара',
            }),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

