import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()


@register.filter
def to_json(value):
    return json.dumps(list(value.values()), cls=DjangoJSONEncoder)
