from django import template
register = template.Library()

@register.filter
def index(obj_list, index):
    return obj_list[index]