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

lass PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('username',)
        labels = {
            'username': 'Usuário',
        }

    def __init__(self, *args, **kwargs):
        self.user_form = kwargs.pop('user_form', None)  # Recebe o UserForm passado como argumento
        super().__init__(*args, **kwargs)
        self.fields.update(self.user_form.fields)  # Atualiza os campos do PerfilForm com os campos do UserForm

    def clean(self):
        cleaned_data = super().clean()
        user_form_data = {key: cleaned_data[key] for key in self.user_form.fields.keys()}
        self.user_form.cleaned_data = user_form_data  # Atualiza o cleaned_data do UserForm

        if not self.user_form.is_valid():
            for field, errors in self.user_form.errors.items():
                self.add_error(field, errors)

        return cleaned_data

    def save(self, commit=True):
        user = self.user_form.save(commit=False)  # Salva o User criado pelo UserForm
        user.set_password(user.password)  # Define a senha usando set_password
        if commit:
            user.save()
        perfil = super().save(commit=False)
        perfil.user = user
        if commit:
            perfil.save()
        return perfil