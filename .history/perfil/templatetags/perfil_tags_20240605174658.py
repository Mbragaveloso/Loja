rom django import template
from crispy_forms.templatetags.crispy_forms_tags import render_crispy as crispy_render_crispy

register = template.Library()

@register.simple_tag
def render_crispy(form):
    return crispy_render_crispy(form)