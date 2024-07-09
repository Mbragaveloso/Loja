from django import forms
from . import models


class PerfilForms(forms.ModelForm):
    class Meta:
        models = models.Perfil
        filter = '__'



class UserForm(forms.ModelForm):
    pass



