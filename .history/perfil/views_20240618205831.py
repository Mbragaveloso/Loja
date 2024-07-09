from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserForm, PerfilForm
from .models import Perfil


class CriarPerfilView(FormView):
    template_name = 'perfil/criar.html'
    form_class = UserForm
    second_form_class = PerfilForm
    success_url = reverse_lazy('produto:lista')  # Redirecionamento após sucesso
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'perfil_form' not in context:
            context['perfil_form'] = self.second_form_class()
        return context

    def form_valid(self, form, perfil_form):
        user = form.save()  # Salva o usuário
        perfil = perfil_form.save(commit=False)
        perfil.user = user
        perfil.save()  # Salva o perfil associado ao usuário
        messages.success(self.request, 'Cadastro realizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, perfil_form):
        messages.error(self.request, 'Erro ao cadastrar usuário. Verifique os dados informados.')
        return self.render_to_response(self.get_context_data(form=form, perfil_form=perfil_form))


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