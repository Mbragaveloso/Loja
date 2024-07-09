from django import template
from crispy_forms.templatetags.crispy_forms_tags import render_crispy as crispy_render_crispy

register = template.Library()

@register.simple_tag
def render_crispy(form):
    return crispy_render_crispy(form)

def render_form_with_crispy(form):
    # Aqui você pode usar o filtro render_crispy para renderizar o formulário
    return render_crispy(form)