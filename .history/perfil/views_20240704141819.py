from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms_perfil import UserForm
from django.contrib import messages
from .forms_perfil import UserForm, PerfilForm, LoginForm

class CriarPerfilView(View):
    template_name = 'perfil/criar.html'
    user_form_class = UserForm
    perfil_form_class = PerfilForm
    
    def setup (self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.contexto ={
            'userform': forms.UserForm(
                data=self.request.POST or None
            ),
            'perfilform': forms.PerfilForm(
                data=self.request.POST or None
            )
        }
        
        self.renderizar = render(
            self.request, self.template_name, self.contexto)
        
        def get(self, *args, **kwargs):
            return self.renderizar

class Atualizar(View):
    template_name = 'perfil/atualizar.html'
    form_class = UserForm

    def get(self, request):
        if request.user.is_authenticated:
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                form = self.form_class(instance=request.user)
                return render(request, self.template_name, {'form': form})
            except Perfil.DoesNotExist:
                # Tratar o caso em que o perfil do usuário não existe
                messages.error(request, 'Perfil não encontrado para este usuário.')
                return redirect('perfil:criarperfil')  # Redirecionar para a página de criação de perfil
        else:
            return redirect('perfil:login')

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Dados atualizados com sucesso!')
                return redirect('produto:resumodacompra')
            else:
                messages.error(request, 'Erro ao atualizar os dados.')
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'perfil/login.html'
    form_class = LoginForm
    user_form_class = UserForm
     
    def get(self, request):
        # Instanciar os formulários vazios
        user_form = UserForm()
        perfil_form = PerfilForm()
        
         # Passar os formulários para o template
        context = {'user_form': user_form, 'perfil_form': perfil_form}
        
        # Renderizar o template com os formulários
        return render(request, self.template_name, context)

class Logout(View):
    def get(self, request):
        carrinho = request.session.get('carrinho')
        logout(request)
        logout(request)
        messages.success(request, 'Você saiu da sua conta. Até logo!')
        return redirect('produto:lista')  # Redireciona após o logout