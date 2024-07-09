from django import forms
from django.contrib.auth.models
from . import models


class PerfilForms(forms.ModelForm):
    class Meta:
        models = models.Perfil
        filter = '__all__'
        exclude = ('usuario'),


class UserForm(forms.ModelForm):
    



