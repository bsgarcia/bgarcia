from django import template
import parameters

register = template.Library()


@register.simple_tag(name='param')
def get_params(key):
    return getattr(parameters, key)


register.filter('param', get_params)

