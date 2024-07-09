from django.template import Library


register = Library()


@re
def formata_preco(val):
    return f'R$ {val: 2f}'.replace('.', ',')