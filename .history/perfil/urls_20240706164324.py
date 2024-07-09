from django.urls import path
from .views import CriarPerfilView, Atualizar, LoginView, Logout

app_name = 'perfil'  # Definindo o namespace

urlpatterns = [
    path('criar/', CriarPerfilView.as_view(), name='criar'),
    path('atualizar/', Atualizar.as_view(), name='atualizar'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    # outras URLs da sua aplicação
]