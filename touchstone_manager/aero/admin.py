from django.contrib import admin

from .models import Material
from .models import MaterialSample
from .models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change) -> None:
        if change:
            if form.changed_data:
                obj.save(update_fields=form.changed_data)
            else:
                obj.save()
        else:
            obj.save()


admin.site.register(Material)
admin.site.register(MaterialSample)
