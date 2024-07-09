from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms_perfil import UserForm, PerfilForm, LoginForm  # Ajuste o import para seus formulários corretos
from django.contrib import messages
from django.http import HttpResponseRedirect

class CriarPerfilView(View):
    template_name = 'perfil/criar.html'
    user_form_class = UserForm
    perfil_form_class = PerfilForm

    def get(self, request):
        if request.user.is_authenticated:
            # Se já estiver autenticado, redirecione para a página desejada
            return redirect('produto:lista')
        
        user_form = self.user_form_class()
        perfil_form = self.perfil_form_class()
        return render(request, self.template_name, {'user_form': user_form, 'perfil_form': perfil_form})

    def post(self, request):
        if request.user.is_authenticated:
            # Se já estiver autenticado, redirecione para a página desejada
            return redirect('produto:lista')
        
        user_form = self.user_form_class(request.POST)
        perfil_form = self.perfil_form_class(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            login(request, user)
            next_url = request.POST.get('next', 'produto:lista')
            return redirect(next_url)
        return render(request, self.template_name, {'user_form': user_form, 'perfil_form': perfil_form})
    
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

class LoginView(View):
    template_name = 'perfil/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('produto:lista')  # Redireciona se já estiver logado
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
                return redirect('produto:lista')  # Redireciona para a página desejada após o login
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, self.template_name, {'form': form})

class Logout(View):
    def get(self, request):
        carrinho = request.session.get('carrinho')
        logout(request)
        messages.success(request, 'Você saiu da sua conta. Até logo!')
        return redirect('produto:lista')  # Redireciona após o logout

