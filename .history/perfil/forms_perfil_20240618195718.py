from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Perfil


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
            raise forms.ValidationError("As senhas não coincidem")

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


class UserForm(BaseForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
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


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('username',)
        labels = {
            'username': 'Usuário',
        }

    def __init__(self, *args, **kwargs):
        self.user_form = kwargs.pop('user_form', None)
        super().__init__(*args, **kwargs)
        if self.user_form:
            self.fields.update(self.user_form.fields)

    def save(self, commit=True):
        user = self.user_form.save(commit=False)
        user.set_password(self.user_form.cleaned_data['password'])
        if commit:
            user.save()
        perfil = super().save(commit=False)
        perfil.user = user
        if commit:
            perfil.save()
        return perfil