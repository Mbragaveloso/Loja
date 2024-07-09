from django import forms
from . import models


class PerfilForms(forms.ModelForm):
    class Meta:
        models = models.Perfil


class UserForm(forms.ModelForm):
    pass



