from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms_perfil import UserForm, PerfilForm
from .models import Perfil


class CriarPerfilView(FormView):
    template_name = 'perfil/criar.html'
    form_class = UserForm
    second_form_class = PerfilForm
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'perfil_form' not in context:
            context['perfil_form'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(request.POST)
        perfil_form = self.second_form_class(request.POST)
        if form.is_valid() and perfil_form.is_valid():
            return self.form_valid(form, perfil_form)
        else:
            return self.form_invalid(form, perfil_form)

    def form_valid(self, form, perfil_form):
        user = form.save() # Salva o usuário
        perfil = perfil_form.save(commit=False)
        perfil.user = user
        perfil.save()  # Salva o perfil associado ao usuário
        messages.success(self.request, 'Cadastro realizado com sucesso!')
        return super().form_valid(form)

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
        return redirect('produto:lista')

class Logout(View):
    def get(self, request, *args, **kwargs):
        carrinho = request.session.get('carrinho')
        logout(request)
        request.session['carrinho'] = carrinho  # Restaura o carrinho na sessão após logout
        request.session.save()
        
        messages.success(request, 'Você saiu da sua conta. Até logo!')
        
        return redirect('produto:lista')