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
    success_url = reverse_lazy('produto:lista')  # Redirecionamento após sucesso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'perfil_form' not in context:
            context['perfil_form'] = PerfilForm()
        return context

    def form_valid(self, form):
        perfil_form = PerfilForm(self.request.POST)
        if perfil_form.is_valid():
            user = form.save()  # Salva o usuário
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()  # Salva o perfil associado ao usuário
            messages.success(self.request, 'Cadastro realizado com sucesso!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        perfil_form = PerfilForm(self.request.POST)
        messages.error(self.request, 'Erro ao cadastrar usuário. Verifique os dados informados.')
        return self.render_to_response(self.get_context_data(form=form, perfil_form=perfil_form))
    

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