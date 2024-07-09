from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)  # Excluindo para definir usuario automaticamente na view ou no formulario

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
        label=sen
    )
    def__init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.usuario = usuario
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
    
    # Clean para validar se o usuario e email estão disponíveis
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