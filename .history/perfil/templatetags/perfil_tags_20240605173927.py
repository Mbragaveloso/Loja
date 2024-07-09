from django import template
from crispy_forms.templatetags.crispy_forms_tags import render_crispy

register = template.Library()

@register.simple_tag
def render_crispy(form):
    return render_crispy(form)