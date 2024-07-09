from  django import template
from django.shortcuts import render

register = template.Library()

@register.simple_tag
def render_crispy(form):
    return render_crispy_form(form)