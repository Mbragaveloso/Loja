from django import template
from crispy_forms.utils import render

register = template.Library()

@register.simple_tag
def render_crispy(form):
    return render_crispy_form(form)