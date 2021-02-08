from django import template

from contactuser.forms import ContactUserForm

register = template.Library()


@register.inclusion_tag('contactuser/tags/form.html')
def contact_form():
    return {'contact_form': ContactUserForm()}
