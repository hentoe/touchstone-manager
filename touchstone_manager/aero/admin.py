from django.contrib import admin

from .models import Material
from .models import MaterialSample
from .models import Measurement

admin.site.register(Material)
admin.site.register(MaterialSample)
admin.site.register(Measurement)
