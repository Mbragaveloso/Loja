from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)

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

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

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

        if self.usuario:
            if usuario_db and usuario_data != usuario_db.username:
                validation_error_msgs['username'] = 'Usuário já existe'
            if email_db and email_data != email_db.email:
                validation_error_msgs['email'] = 'E-mail já existe'
        else:
            if usuario_db:
                validation_error_msgs['username'] = 'Usuário já existe'
            if email_db:
                validation_error_msgs['email'] = 'E-mail já existe'

        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)

        return cleaned_data

class CriarPerfilView(View):
    template_name = 'perfil/criar.html'

    def get(self, request):
        user_form = UserForm()
        perfil_form = PerfilForm()
        context = {'user_form': user_form, 'perfil_form': perfil_form}
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            messages.success(request, "Perfil criado com sucesso!")
            return redirect('perfil:criar')  # Altere para a URL desejada
        else:
            context = {'user_form': user_form, 'perfil_form': perfil_form}
            return render(request, self.template_name, context)
    
class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')

class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:criar')

        usuario = authenticate(
            self.request, username=username, password=password)

        if not usuario:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:criar')

        login(self.request, user=usuario)

        messages.success(
            self.request,
            'Você fez login no sistema e pode concluir sua compra.'
        )
        return redirect('produto:carrinho')

class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        logout(self.request)

        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        return redirect('produto:lista')

