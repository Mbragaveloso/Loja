from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms_perfil import UserForm, PerfilForm
from .models import Perfil

class LoginView(View):
    template_name = 'login.html'

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

class CriarPerfilView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        user_form = UserForm()
        perfil_form = PerfilForm()
        context = {'user_form': user_form, 'perfil_form': perfil_form}
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()

            messages.success(request, "Perfil criado com sucesso!")
            return redirect('perfil:login')

        context = {'user_form': user_form, 'perfil_form': perfil_form}
        return render(request, self.template_name, context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout realizado com sucesso!")
        return redirect('perfil:login')

class Atualizar(View):
    def get(self, request):
        return HttpResponse('Atualizar')  # Implementar funcionalidade de atualização se necessário