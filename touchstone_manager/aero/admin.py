from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Material
from .models import MaterialSample
from .models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ["aero_material", "measurement_date", "mean_s21"]
    search_fields = ["aero_material__name"]
    readonly_fields = ["created", "modified", "measurement_data", "mean_s21"]

    fieldsets = (
        (None, {"fields": ("aero_material",)}),
        (_("File"), {"fields": ("measurement_file", "measurement_date", "mean_s21")}),
        (_("Important dates"), {"fields": ("created", "modified")}),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["name", "short_name"]
    search_fields = ["name", "short_name"]
    readonly_fields = ["created", "modified"]

    fieldsets = (
        (None, {"fields": ("name", "short_name", "description")}),
        (_("Important dates"), {"fields": ("created", "modified")}),
    )


@admin.register(MaterialSample)
class MaterialSampleAdmin(admin.ModelAdmin):
    search_fields = ["name", "material__name"]
    readonly_fields = ["created", "modified"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "sample_number",
                    "material",
                    "thickness",
                    "weight",
                    "infiltrations",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("created", "modified")}),
    )
