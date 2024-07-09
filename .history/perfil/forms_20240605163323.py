from django import forms
from django.contrib.auth.models import User
from . import models

class PerfilForms(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',) # Excluindo para definir usuario altomaticamente na view ou no formulario


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
    
    # Clwar_username para validar se o usuario e emails estão  disponíveis
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists(): 
            raise ValidationError("Este nome de usuário já está em uso. Por favor, escolha outro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este endereço de e-mail já está em uso. Por favor, escolha outro.")
        return email