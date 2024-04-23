from django.db import models
from django.utils.translation import gettext_lazy as _

from touchstone_manager.utils.models import TimeStampedModel


class Material(TimeStampedModel):
    """Model for Materials, e.g. Graphene"""

    name = models.CharField(_("Name of Material"), max_length=100)
    short_name = models.CharField(_("Abbreviated name of Material"), max_length=30)
    description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.name


class MaterialSample(TimeStampedModel):
    """Material specimen for making measurements."""

    name = models.CharField(_("Name of Sample"), max_length=255)
    sample_number = models.IntegerField(_("Number of Sample"), unique=True)
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name=_("Material"),
    )
    thickness = models.FloatField(_("Thickness in mm"))
    weight = models.FloatField(_("Weight in mg"))


class Measurement(TimeStampedModel):
    """Measurement performed on AeroMaterials."""

    aero_material = models.ForeignKey(
        MaterialSample,
        on_delete=models.CASCADE,
        verbose_name=_("Device under Test"),
    )
    measurement_date = models.DateField(_("Measurement date"))
    mean_s21 = models.FloatField(_("Mean S21 over frequency range"))
