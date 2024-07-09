from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms_perfil import UserForm
from django.contrib import messages
from .forms_perfil import LoginForm
from .models import Perfil  # Certifique-se de importar o modelo Perfil

class CriarPerfilView(View):
    template_name = 'perfil/criar.html'
    form_class = UserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Crie um usuário primeiro
            user = form.save(commit=False)
            user.save()
            # Em seguida, crie um perfil associado a esse usuário
            perfil = Perfil(usuario=user)
            perfil.cpf = form.cleaned_data['cpf']  # Exemplo de como salvar o CPF do formulário
            perfil.endereco = form.cleaned_data['endereco']
            perfil.numero = form.cleaned_data['numero']
            perfil.complemento = form.cleaned_data['complemento']
            perfil.bairro = form.cleaned_data['bairro']
            perfil.cidade = form.cleaned_data['cidade']
            perfil.estado = form.cleaned_data['estado']
            perfil.save()
            messages.success(request, 'Perfil criado com sucesso!')
            return redirect('produto:lista')  # Substitua por uma URL adequada
        return render(request, self.template_name, {'form': form})
    
class Atualizar(View):
    template_name = 'perfil/atualizar.html'
    form_class = UserForm

    def get(self, request):
        if request.user.is_authenticated:
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                form = self.form_class(instance=request.user)
                return render(request, self.template_name, {'form': form})
            except Perfil.DoesNotExist:
                # Tratar o caso em que o perfil do usuário não existe
                messages.error(request, 'Perfil não encontrado para este usuário.')
                return redirect('perfil:criarperfil')  # Redirecionar para a página de criação de perfil
        else:
            return redirect('perfil:login')

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Dados atualizados com sucesso!')
                return redirect('produto:resumodacompra')
            else:
                messages.error(request, 'Erro ao atualizar os dados.')
        return render(request, self.template_name, {'form': form})

class Login(View):
    template_name = 'perfil/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('produto:lista') # Redireciona se o usuário já estiver autenticado
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('produto:lista') # Redireciona para a página desejada após o login
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, self.template_name, {'form': form})

class Logout(View):
    def get(self, request):
        carrinho = request.session.get('carrinho')
        logout(request)
        logout(request)
        messages.success(request, 'Você saiu da sua conta. Até logo!')
        return redirect('produto:lista')  # Redireciona após o logout