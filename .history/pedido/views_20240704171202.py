from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from .models import Pedido  # Importe seu modelo de pedido aqui

class ListaPedidos(ListView):
    model = Pedido
    template_name = 'pedido/lista_pedidos.html'  # Nome do seu template de lista de pedidos
    context_object_name = 'pedidos'  # Nome do contexto que será passado para o template

class Pagar(View):
    def get(swlf, *args, **kwargs):
        return HttpResponse('Pagar')

class SalvarPedido(View):
     def get(swlf, *args, **kwargs):
        return HttpResponse('Fechar Pedido')


class Detalhe(View):
     def get(swlf, *args, **kwargs):
        return HttpResponse('Detalhe')

