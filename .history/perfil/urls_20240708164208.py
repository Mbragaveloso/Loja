# urls.py
from django.urls import path
from .views import CriarPerfilView, Atualizar, LoginView, LogoutView

urlpatterns = [
    path('criarperfil/', CriarPerfilView.as_view(), name='criarperfil'),
    path('atualizarperfil/', Atualizar.as_view(), name='atualizarperfil'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]