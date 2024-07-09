from django import template
from django.views.generic import DetailView
from .templatetags import models

register = template.Library()

@register.filter
def minha_tag_personalizada(valor):
    return f'{valor:.2f}'.replace('.', ',')

class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'

    def get_queryset(self):
        return models.Produto.objects.all()