from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Material
from .models import MaterialSample
from .models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ["aero_material", "measurement_date", "mean_s21"]
    search_fields = ["aero_material__name"]
    readonly_fields = ["created", "modified"]

    fieldsets = (
        (None, {"fields": ("aero_material",)}),
        (_("File"), {"fields": ("measurement_file", "measurement_date", "mean_s21")}),
        (_("Important dates"), {"fields": ("created", "modified")}),
    )

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
