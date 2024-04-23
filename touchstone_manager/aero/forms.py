from django import forms

from touchstone_manager.aero.models import Measurement


class AddMeasurement(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ["aero_material", "measurement_date"]
