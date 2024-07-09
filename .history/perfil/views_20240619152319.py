from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from .forms_perfil import UserForm, PerfilForm
from django.urls import reverse_lazy


class CriarPerfilView(View):
    template_name = 'perfil/criar.html'
    form_class = UserForm
  
 
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

     def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('produto:resumodacompra')
            else:
                messages.error(request, 'Falha ao realizar o cadastro.')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Erro no formulário.')
            return render(request, self.template_name, {'form': form})
        
        
class Atualizar(View):
    template_name = 'perfil/atualizar.html'

    def get(self, request):
        perfil = Perfil.objects.get(user=request.user)  # Obtém o perfil do usuário logado
        form = AtualizarPerfilForm(instance=perfil)  # Cria o formulário com os dados do perfil
        
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        perfil = Perfil.objects.get(user=request.user)  # Obtém o perfil do usuário logado
        form = AtualizarPerfilForm(request.POST, instance=perfil)  # Preenche o formulário com os dados do perfil atual
        
        if form.is_valid():
            form.save()  # Salva as alterações no perfil
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('produto:lista')  # Redireciona para a lista de produtos após a atualização

        # Se o formulário não for válido, retorna o template com os erros
        return render(request, self.template_name, {'form': form})


class Login(View):
    template_name = 'perfil/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('produto:resumodacompra')
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
                return redirect('produto:resumodacompra')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Erro no formulário.')
            return render(request, self.template_name, {'form': form})

class Logout(View):
    def get(self, request, *args, **kwargs):
        carrinho = request.session.get('carrinho')
        logout(request)
        request.session['carrinho'] = carrinho  # Restaura o carrinho na sessão após logout
        request.session.save()

        messages.success(request, 'Você saiu da sua conta. Até logo!')
        
        return redirect('produto:lista')