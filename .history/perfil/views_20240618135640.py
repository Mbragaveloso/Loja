from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms_perfil import UserForm, PerfilForm
from .models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)

class CriarPerfilView(View):
    template_name = 'perfil/criar.html'  # Atualize para 'criar.html'

    def get(self, request):
        user_form = UserForm()
        perfil_form = PerfilForm()
        context = {'user_form': user_form, 'perfil_form': perfil_form}
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
                        # Salvando o formulário do usuário
            user = user_form.save()
            
            # Salvando o formulário de perfil associado ao usuário
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user  # Associando o perfil ao usuário criado
            perfil.save()

             # Mensagem de sucesso
            messages.success(request, "Perfil criado com sucesso!")

            return redirect('/')  # Redirecionar para a página inicial após o sucesso

            # Se o formulário não for válido, renderizar novamente a página com os formulários e mensagens de erro
        context = {'user_form': user_form, 'perfil_form': perfil_form}
        return render(request, self.template_name, context)
        

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
