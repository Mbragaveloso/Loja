from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class BaseForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não coincidem")

        if password and len(password) < 6:
            raise forms.ValidationError("A senha deve ter pelo menos 6 caracteres")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'password' in self.cleaned_data:
            instance.set_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance

class UserForm(BaseForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='Digite pelo menos 6 caracteres'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário',
            'email': 'E-mail',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class PerfilForm(BaseForm):
    class Meta:
        model = Perfil
        fields = ('first_name', 'last_name', 'email')  # Defina os campos relevantes para o Perfil
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
