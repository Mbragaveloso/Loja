from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import copy

from . import models
from . import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def get_context_data(self, **kwargs):
        contexto = {}

        contexto['userform'] = forms.UserForm(
            data=self.request.POST or None,
            usuario=self.request.user if self.request.user.is_authenticated else None,
            instance=self.request.user if self.request.user.is_authenticated else None,
        )

        contexto['perfilform'] = forms.PerfilForm(
            data=self.request.POST or None,
        )

        return contexto

    def get(self, request, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        contexto = self.get_context_data(**kwargs)  # chame super().get_context_data()
        return render(request, self.template_name, contexto)

    def post(self, request, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        contexto = self.get_context_data(**kwargs)  # chame super().get_context_data()

        userform = contexto['userform']
        perfilform = contexto['perfilform']

        if userform.is_valid() and perfilform.is_valid():
            # Lógica de processamento do formulário aqui
            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password')
            email = userform.cleaned_data.get('email')
            first_name = userform.cleaned_data.get('first_name')
            last_name = userform.cleaned_data.get('last_name')

            # Processar os dados do perfil
            # Exemplo: Criar ou atualizar um perfil
            perfil = perfilform.save(commit=False)
            perfil.usuario = request.user  # Se houver usuário logado
            perfil.save()

            # Processar os dados do usuário
            if request.user.is_authenticated:
                usuario = request.user
            else:
                usuario = userform.save(commit=False)
                usuario.set_password(password)
                usuario.save()

            # Autenticar o usuário se não estiver autenticado
            if not request.user.is_authenticated:
                usuario = authenticate(request, username=username, password=password)
                if usuario is not None:
                    login(request, usuario)
                else:
                    messages.error(request, 'Falha na autenticação')

            # Redirecionar para a página desejada após o processamento
            return redirect('perfil:criar_sucesso')

        # Se o formulário não for válido, renderizar novamente a página com os erros
        return render(request, self.template_name, contexto)


class Criar(BasePerfil):
    def post(self, request, *args, **kwargs):
        contexto = self.get_context_data()  # Obtenha o contexto dos formulários

        userform = contexto['userform']
        perfilform = contexto['perfilform']

        password = None  # Definir password inicialmente como None

        if userform.is_valid():
            # Lógica de processamento do formulário aqui
            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password')  # Atribuir o valor de password se o formulário for válido
            email = userform.cleaned_data.get('email')
            first_name = userform.cleaned_data.get('first_name')
            last_name = userform.cleaned_data.get('last_name')

        # usuario logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)

            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

        # usuario nao log
        else:
            usuario = userform.save(commit=False)
            usuario.set_password(password)  # Definir a senha apenas se ela for fornecida
            usuario.save()

            perfil = perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:  # Verificar se a senha foi fornecida
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )

            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        return render(request, self.template_name, contexto)
    
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