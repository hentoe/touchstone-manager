import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile

register = template.Library()


@register.filter
def to_json(value):
    if hasattr(value, "all"):
        # for QuerySet of objects
        data = [obj_to_dict(obj) for obj in value]
    else:
        # for single object
        data = obj_to_dict(value)
    return json.dumps(data, cls=DjangoJSONEncoder)


def obj_to_dict(obj):
    data = {}
    for field in obj._meta.get_fields():  # noqa: SLF001
        if field.is_relation and field.many_to_one:
            related_obj = getattr(obj, field.name, None)
            if related_obj:
                data[field.name] = obj_to_dict(related_obj)
            else:
                data[field.name] = None
        else:
            value = getattr(obj, field.name, None)
            if isinstance(value, FieldFile):
                data[field.name] = value.url if value else None
            else:
                data[field.name] = value
    return data
