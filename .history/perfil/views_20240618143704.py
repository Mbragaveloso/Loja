from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms_perfil import UserForm, PerfilForm
from .models import Perfil


class CriarPerfilView(CreateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'perfil/criar_perfil.html'  # Substitua com o seu template
    success_url = '/perfil/sucesso/'  # Substitua com a URL de sucesso após criar o perfil
    
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirecione para a página de sucesso, por exemplo:
            return redirect('perfil:criar')  # ou para outra URL após salvar o perfil
    else:
        form = PerfilForm()

    return render(request, 'seu_template.html', {'form': form})

class Atualizar(View):
    def get(self, request):
        return HttpResponse('Atualizar')  # Implementar funcionalidade de atualização se necessário

class LoginView(View):
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

class LogoutView(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        logout(self.request)

        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        return redirect('produto:lista')
