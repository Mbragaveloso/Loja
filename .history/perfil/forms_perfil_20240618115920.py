from django import forms
from .models import Perfil
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
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
    
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('idade', 'data_nascimento', 'cpf', 'endereco', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'estado')
        labels = {
            'idade': 'Idade',
            'data_nascimento': 'Data de Nascimento',
            'cpf': 'CPF',
            'endereco': 'Endereço',
            'numero': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cep': 'CEP',
            'cidade': 'Cidade',
            'estado': 'Estado',
        }
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}), 
        }
        def criar_perfil(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            # Salvar os formulários ou realizar outra lógica
            user_form.save()
            perfil_form.save()
    else:
        user_form = UserForm()
        perfil_form = PerfilForm()
    
    context = {
        'user_form': user_form,
        'perfil_form': perfil_form,
    }
    return render(request, 'criar.html', context)