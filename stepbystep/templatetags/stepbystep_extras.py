# coding: utf8
#import re
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def code_strong(value):
    safe_value = mark_safe(value)
    #m = re.match('(?P<pre>.*)[pre](?P<code>.*)[/pre](?P<end>.*)', value)
    value = safe_value.replace('[code]', '<code>').replace('[/code]', '</code>')
    value = value.replace('[pre]', '<pre>').replace('[/pre]', '</pre>')
    value = value.replace('[strong]', '<strong>').replace('[/strong]', '</strong>')
    value = value.replace('[/br]', '</br>')
    value = value.replace('[p]', '<p>').replace('[/p]', '</p>')
    return value
