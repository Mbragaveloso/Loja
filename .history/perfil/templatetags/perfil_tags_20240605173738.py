from  django 

register = template.Library()

@register.simple_tag
def render_crispy(form):
    return render_crispy_form(form)