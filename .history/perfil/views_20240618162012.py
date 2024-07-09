from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms_perfil import UserForm, PerfilForm
from .models import Perfil

class CriarPerfilView(View):
    def get(self, request):
        perfil_form = PerfilForm()
        return render(request, 'perfil/criar.html', {'perfil_form': perfil_form})

    def post(self, request):
        perfil_form = PerfilForm(request.POST)
        if perfil_form.is_valid():
            perfil_form.save()
            return redirect('perfil:sucesso')
        return render(request, 'perfil/criar.html', {'perfil_form': perfil_form})

class Atualizar(View):
    def get(self, request):
        return HttpResponse('Atualizar')  # Implementar funcionalidade de atualização se necessário


class Login(View):
    template_name = 'perfil/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('perfil:login')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('perfil:login')

        login(request, user)
        messages.success(request, 'Login realizado com sucesso!')
        return redirect('home')

class Logout(View):
    def get(self, request, *args, **kwargs):
        carrinho = request.session.get('carrinho')
        logout(request)
        request.session['carrinho'] = carrinho  # Restaura o carrinho na sessão após logout
        request.session.save()
        return redirect('produto:lista')