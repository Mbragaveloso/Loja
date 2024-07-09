from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

from . import models
from . import forms_perfil 

class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def get_context_data(self):
        userform_kwargs = {
            'data': self.request.POST or None,
            'usuario': self.request.user if self.request.user.is_authenticated else None,
            'instance': self.request.user if self.request.user.is_authenticated else None,
        }
        perfilform_kwargs = {
            'data': self.request.POST or None,
            'instance': self.perfil,
        }

        context = {
            'userform': forms_perfil.UserForm(**userform_kwargs),
            'perfilform': forms_perfil.PerfilForm(**perfilform_kwargs),
        }

        return context

    def render_with_context(self, context):
        return render(self.request, self.template_name, context)

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

        self.contexto = self.get_context_data()
        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = self.render_with_context(self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class CriarPerfilView(BasePerfil):
    def post(self, *args, **kwargs):
        self.setup(*args, **kwargs)

        if not self.contexto['userform'].is_valid() or not self.contexto['perfilform'].is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos os campos foram preenchidos corretamente.'
            )
            return self.renderizar

        username = self.contexto['userform'].cleaned_data.get('username')
        password = self.contexto['userform'].cleaned_data.get('password')
        email = self.contexto['userform'].cleaned_data.get('email')
        first_name = self.contexto['userform'].cleaned_data.get('first_name')
        last_name = self.contexto['userform'].cleaned_data.get('last_name')

        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)

            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                self.contexto['perfilform'].cleaned_data['usuario'] = usuario
                perfil = models.Perfil(**self.contexto['perfilform'].cleaned_data)
                perfil.save()
            else:
                perfil = self.contexto['perfilform'].save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        # Usário não logado (novo)
        else:
            usuario = self.contexto['userform'].save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.contexto['perfilform'].save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(self.request, username=usuario.username, password=password)

            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        messages.success(
            self.request,
            'Você fez login e pode concluir sua compra.'
        )

        return redirect('produto:carrinho')


class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class LoginView(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:criar')

        usuario = authenticate(self.request, username=username, password=password)

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