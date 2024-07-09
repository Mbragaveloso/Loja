
from django.urls import path
from perfil.views import CriarPerfilView, Atualizar, LoginView, Logout  # Certifique-se de importar as views corretamente

urlpatterns = [
    path('perfil/criarperfil/', CriarPerfilView.as_view(), name='criarperfil'),
    path('perfil/atualizarperfil/', Atualizar.as_view(), name='atualizarperfil'),
    path('perfil/login/', LoginView.as_view(), name='login'),
    path('perfil/logout/', Logout.as_view(), name='logout'),
]