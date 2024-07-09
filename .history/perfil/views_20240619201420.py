from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from .forms_perfil import UserForm, LoginForm , PerfilForm # importando os formulario


class CriarPerfilView(View):
    template_name = 'perfil/criar.html'
    form_class = UserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('produto:resumodacompra')
            else:
                messages.error(request, 'Falha ao realizar o cadastro.')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Erro no formulário.')
            return render(request, self.template_name, {'form': form})


class Atualizar(View):
    template_name = 'perfil/atualizar.html'
    form_class = UserForm

    def get(self, request):
        if request.user.is_authenticated:
            perfil = Perfil.objects.get(user=request.user)
            form = self.form_class(instance=request.user)
            return render(request, self.template_name, {'form': form})
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
        else:
            return redirect('perfil:perfil')


class Login(View):
    template_name = 'perfil/login.html'
    form_class = LoginForm  # Use o formulário de login correto

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('produto:resumodacompra')  # Redireciona se o usuário já estiver autenticado
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
                return redirect('produto:resumodacompra')  # Redireciona após o login bem-sucedido
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        # Se o formulário não for válido, ou se o login falhar, renderize o template com o formulário e mensagens de erro
        return render(request, self.template_name, {'form': form})
    

class Logout(View):
    def get(self, request, *args, **kwargs):
        carrinho = request.session.get('carrinho')
        logout(request)
        request.session['carrinho'] = carrinho  # Restaura o carrinho na sessão após logout
        request.session.save()

        messages.success(request, 'Você saiu da sua conta. Até logo!')

        return redirect('produto:lista')