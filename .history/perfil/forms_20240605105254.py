from django import forms
from . import models


class PerfilForms(forms.ModelForm):
    class Meta:
        models = models.Perfil
        filter = '__all__'



class UserForm(forms.ModelForm):
    pass



