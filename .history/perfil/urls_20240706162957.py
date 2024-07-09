from django.urls import path
from .views import CriarPerfilView, Atualizar, LoginView, Logout

urlpatterns = [
    path('perfil/criar/', CriarPerfilView.as_view(), name='criar'),
    path('perfil/atualizar/', Atualizar.as_view(), name='atualizar'),
    path('perfil/login/', LoginView.as_view(), name='login'),
    path('perfil/logout/', Logout.as_view(), name='logout'),
    # outras URLs da sua aplicação
]