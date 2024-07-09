from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='Digite pelo menos 6 caracteres'
    )

    password2 = forms.CharField(
        required=False,
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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não coincidem")

        if password and len(password) < 6:
            raise forms.ValidationError("A senha deve ter pelo menos 6 caracteres")

        usuario_data = cleaned_data.get('username')
        email_data = cleaned_data.get('email')
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        validation_error_msgs = {}

        if self.instance:
            if usuario_db and usuario_data != self.instance.username:
                validation_error_msgs['username'] = 'Usuário já existe'
            if email_db and email_data != self.instance.email:
                validation_error_msgs['email'] = 'E-mail já existe'
        else:
            if usuario_db:
                validation_error_msgs['username'] = 'Usuário já existe'
            if email_db:
                validation_error_msgs['email'] = 'E-mail já existe'

        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)

        return cleaned_data

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['idade', 'data_nascimento', 'cpf', 'endereco', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado']