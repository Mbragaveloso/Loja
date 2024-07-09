from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForms(forms.ModelForm):
    class Meta:
        models = models.Perfil
        filter = '__all__'
        exclude = ('usuario'),


class UserForm(forms.ModelForm):
    models = User
    fields = ()
    



