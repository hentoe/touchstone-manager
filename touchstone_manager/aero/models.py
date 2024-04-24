from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import gettext_lazy as _

from touchstone_manager.utils.models import TimeStampedModel

fs = FileSystemStorage(location="/media/uploads")


class Material(TimeStampedModel):
    """Model for Materials, e.g. Graphene"""

    class Meta:
        verbose_name = _("material")
        verbose_name_plural = _("materials")

    name = models.CharField(_("Name of Material"), max_length=100)
    short_name = models.CharField(
        _("Abbreviated name of Material"),
        max_length=30,
    )
    description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.name


class MaterialSample(TimeStampedModel):
    """Material specimen for making measurements."""

    class Meta:
        verbose_name = _("material sample")
        verbose_name_plural = _("material samples")

    name = models.CharField(_("Name of Sample"), max_length=255)
    sample_number = models.IntegerField(_("Number of Sample"), unique=True)
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name=_("Material"),
    )
    thickness = models.FloatField(_("Thickness in mm"))
    weight = models.FloatField(_("Weight in mg"))
    infiltrations = models.IntegerField(
        _("Number of infiltrations with Nanomaterial"),
        default=0,
    )

    def __str__(self):
        return self.name


class Measurement(TimeStampedModel):
    """Measurement performed on AeroMaterials."""

    class Meta:
        verbose_name = _("measurement")
        verbose_name_plural = _("measurements")

    aero_material = models.ForeignKey(
        MaterialSample,
        on_delete=models.CASCADE,
        verbose_name=_("Device under Test"),
    )
    measurement_date = models.DateField(_("Measurement date"))
    measurement_file = models.FileField(
        upload_to="measurements/",
        storage=fs,
        blank=True,
    )
    mean_s21 = models.FloatField(_("Mean S21 over frequency range"))

    def __str__(self):
        return f"{self.aero_material} on {self.measurement_date}"
