from django import template

from mmorpg.models import Ads

register = template.Library()


@register.filter()
def ads_len(value):
    page_value = str(len(value))
    total_value = str(len(Ads.objects.all()))
    return f' {page_value} из {total_value}'


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
