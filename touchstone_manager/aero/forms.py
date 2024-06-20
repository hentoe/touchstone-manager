from django import forms
from django.utils.translation import gettext_lazy as _

from touchstone_manager.aero.models import Material


class MaterialSampleFilterForm(forms.Form):
    """Material Filter Form"""

    material = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all().order_by("name"),
        required=False,
        label=_("Material"),
        widget=forms.CheckboxSelectMultiple,
    )

    thickness_from = forms.FloatField(
        required=False,
        label=_("Thickness From"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )
    thickness_to = forms.FloatField(
        required=False,
        label=_("Thickness To"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )

    weight_from = forms.FloatField(
        required=False,
        label=_("Weight From"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )
    weight_to = forms.FloatField(
        required=False,
        label=_("Weight To"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )

    infiltrations_from = forms.IntegerField(
        required=False,
        label=_("Infiltrations From"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )
    infiltrations_to = forms.IntegerField(
        required=False,
        label=_("Infiltrations To"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )

    def clean(self):
        cleaned_data = super().clean()

        thickness_from = cleaned_data.get("thickness_from")
        thickness_to = cleaned_data.get("thickness_to")
        if thickness_from and thickness_to and thickness_from >= thickness_to:
            raise forms.ValidationError(
                _("Thickness From must be less than Thickness To"),
            )

        weight_from = cleaned_data.get("weight_from")
        weight_to = cleaned_data.get("weight_to")
        if weight_from and weight_to and weight_from >= weight_to:
            raise forms.ValidationError(_("Weight From must be less than Weight To"))

        infiltrations_from = cleaned_data.get("infiltrations_from")
        infiltrations_to = cleaned_data.get("infiltrations_to")
        if (
            infiltrations_from
            and infiltrations_to
            and infiltrations_from >= infiltrations_to
        ):
            raise forms.ValidationError(
                _("Infiltrations From must be less than Infiltrations To"),
            )

        return cleaned_data


class MeasurementFilterForm(forms.Form):
    """Measurement Filter Form"""

    material = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all().order_by("name"),
        required=False,
        label=_("Material"),
        widget=forms.CheckboxSelectMultiple,
    )

    mean_s21_from = forms.FloatField(
        required=False,
        label=_("Mean S21 From"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )
    mean_s21_to = forms.FloatField(
        required=False,
        label=_("Mean S21 To"),
        widget=forms.NumberInput(attrs={"type": "number"}),
    )

    def clean(self):
        cleaned_data = super().clean()

        mean_s21_from = cleaned_data.get("mean_s21_from")
        mean_s21_to = cleaned_data.get("mean_s21_to")
        if mean_s21_from and mean_s21_to and mean_s21_from >= mean_s21_to:
            raise forms.ValidationError(
                _("Mean S21 From must be less than Mean S21 To"),
            )

        return cleaned_data
