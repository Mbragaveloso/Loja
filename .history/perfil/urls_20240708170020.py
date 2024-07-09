from django.urls import path
from perfil.views import CriarPerfilView, Atualizar, LoginView, LogoutView  # Certifique-se de importar as views corretamente

app_name = 'perfil'

urlpatterns = [
    path('perfil/criarperfil/', CriarPerfilView.as_view(), name='criarperfil'),
    path('perfil/atualizarperfil/', Atualizar.as_view(), name='atualizarperfil'),
    path('perfil/login/', LoginView.as_view(), name='login'),
    path('perfil/logout/', LogoutView.as_view(), name='logout'),
]