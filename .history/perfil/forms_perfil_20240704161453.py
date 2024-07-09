from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Perfil
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BaseForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='Digite pelo menos 6 caracteres'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirmação de senha'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password', _('As senhas não coincidem'))
            self.add_error('password2', _('As senhas não coincidem'))

        if password and len(password) < 6:
            raise forms.ValidationError("A senha deve ter pelo menos 6 caracteres")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            instance.set_password(password)
        if commit:
            instance.save()
        return instance

class UserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Usuário',
        help_text='Máximo de 150 caracteres. Apenas letras, números e @/./+/-/_ são permitidos.'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='Digite pelo menos 6 caracteres.'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmação de senha'
    )
    email = forms.EmailField(
        label='E-mail',
        help_text='Digite um endereço de e-mail válido.'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalnum() and '@' not in username and '.' not in username and '+' not in username and '-' not in username and '_' not in username:
            raise ValidationError(_('O nome de usuário pode conter apenas letras, números e @/./+/-/_.'))
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError(_('As senhas não coincidem.'))
        if password and len(password) < 6:
            raise ValidationError(_('A senha deve ter pelo menos 6 caracteres.'))
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha')
    
    
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['cpf', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
