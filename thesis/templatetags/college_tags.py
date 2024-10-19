from django import template
from thesis.models import College  # Import your Schedule model

register = template.Library()

@register.simple_tag
def get_all_college():
    return College.objects.values('id', 'code', 'college_name').distinct().order_by('id')

