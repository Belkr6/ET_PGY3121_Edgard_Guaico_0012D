from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import ModelChoiceField
from django.forms.widgets import Widget
from .models import Categoria, Alimentos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 


class ItemForm(forms.ModelForm):
    class Meta:
        model = Alimentos
        fields = ['itemid', 'marca', 'tipodeal', 'tmascot', 'imagen', 'categoria', 'precio','cantidad_disponible','descripcion']
        widgets = {
            'itemid': forms.TextInput(attrs={'placeholder': 'Ingrese un Id', 'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'placeholder': 'Ingrese un Nombre', 'class': 'form-control'}),
            'tipodeal': forms.TextInput(attrs={'placeholder': 'Ingrese un Alimento', 'class': 'form-control'}),
            'tmascot': forms.TextInput(attrs={'placeholder': 'Ingrese el Animal', 'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control','id':'categoria'}),
            'precio': forms.NumberInput(attrs={'placeholder': 'Ingrese el precio', 'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'placeholder': 'Ingrese el Stock', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'class': 'form-control'}),
            
        }
        labels = {
            'itemid': "Item Id",
            'marca': "Nombre",
            'tipodeal': "Tipo de Alimento",
            'tmascot': "Para:",
            'imagen': "Imagen",
            'categoria': "Categoria",
            'precio':"Precio",
            'cantidad_disponible': "Stock",
            'descripcion':"Descripcion",
            
        }
        
class RegistroUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
