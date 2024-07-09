from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, PerfilForm
from django.contrib.auth.models import User
import copy

from . import models
from . import forms

class BasePerfil(View):
    template_name = 'perfil/criar.html'
    
    def get_context_data(self, **kwargs):
        return {
            'user_form': forms.UserForm(data=self.request.POST ),
            'perfil_form': forms.PerfilForm(data=self.request.POST)
        }
    
    def get(self, request, *args, **kwargs):
        contexto = self.get_context_data()
        return render(request, self.template_name, contexto)
    
    def post(self, request, *args, **kwargs):
        user_form = forms.UserForm(request.POST)
        perfil_form = forms.PerfilForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            # Faça algo com os dados dos formulários (salvar no banco de dados, por exemplo)
            # ...
            return HttpResponse('Dados salvos com sucesso!')  # ou redirecione para outra página
        else:
            contexto = self.get_context_data()
            return render(request, self.template_name, contexto)

class Criar(View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        perfil_form = PerfilForm()
        return render(request, 'perfil/criar.html', {'user_form': user_form, 'perfil_form': perfil_form})

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('perfil:login')

        return render(request, 'perfil/criar.html', {'user_form': user_form, 'perfil_form': perfil_form})


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