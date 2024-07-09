from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class BaseForm(forms.ModelForm):
    class Meta:
        abstract = True  # Define o formulário como abstrato, para que não seja criado diretamente

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not valida_cpf(cpf):
            raise forms.ValidationError('Digite um CPF válido')
        return cpf

    def clean_cep(self):
        cep = self.cleaned_data['cep']
        if re.search(r'[^0-9]', cep) or len(cep) != 8:
            raise forms.ValidationError('CEP inválido, digite 8 dígitos do CEP.')
        return cep

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

    class Meta(BaseForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuário',
            'email': 'E-mail',
        }
        help_texts = {
            'username': 'O nome de usuário deve conter no máximo 150 caracteres. Apenas letras, números e @/./+/-/_ são permitidos.',
            'password': 'Digite pelo menos 6 caracteres.',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não coincidem")

        if password and len(password) < 6:
            raise forms.ValidationError("A senha deve ter pelo menos 6 caracteres")

        return cleaned_data

class PerfilForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Perfil
        fields = ('cpf', 'cep')  # Adicione outros campos de Perfil conforme necessário


