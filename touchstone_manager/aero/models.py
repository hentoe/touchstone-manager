from datetime import datetime
from pathlib import Path

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import get_default_timezone
from django.utils.translation import gettext_lazy as _
from skrf import Network

from touchstone_manager.utils.models import TimeStampedModel


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

    def get_absolute_url(self):
        """Returns the URL to access a particular material instance."""
        return reverse("aero:material-detail", args=[str(self.id)])


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

    def get_absolute_url(self):
        """Returns the URL to access a particular sample instance."""
        return reverse("aero:sample-detail", args=[str(self.id)])


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
    measurement_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Measurement date and time"),
        help_text=_(
            "Initially set to the current date and time. "
            "Will be updated with the date and time from the imported file.",
        ),
    )
    measurement_file = models.FileField(
        upload_to="uploads/measurements/",
        blank=True,
        verbose_name=_("Touchstone file"),
    )
    mean_s21 = models.FloatField(
        _("Mean S21 over frequency range"),
        default=0,
        editable=False,
    )
    measurement_data = models.JSONField(default=dict, editable=False)

    def save(self, *args, **kwargs):
        if self.measurement_file:
            try:
                self.process_file()
            except FileNotFoundError:
                super().save(*args, **kwargs)
                self.process_file()
        super().save(*args, **kwargs)

    def process_file(self):
        if self.measurement_file:
            try:
                network = Network(self.measurement_file.path)
                frequencies = network.f
                s21 = network.s21.s_db
                self.mean_s21 = s21.mean()
                self.measurement_data["frequency"] = frequencies.tolist()
                self.measurement_data["s21"] = list(s21.flatten())
                self.measurement_date = self.extract_date_from_file()
            except ValueError:
                self.measurement_file = ""

    def extract_date_from_file(self):
        if self.measurement_file:
            file_path = Path(self.measurement_file.path)
            with file_path.open() as file:
                # Date is third line in file, remove first to chars
                date_string = file.readlines()[2].strip()[2:]
            date_time_obj = datetime.strptime(
                date_string,
                "%m/%d/%Y %I:%M:%S %p",
            ).astimezone(get_default_timezone())

        return date_time_obj

    def __str__(self):
        return _("%(aero_material)s on %(date)s") % {
            "aero_material": self.aero_material.name,
            "date": self.measurement_date,
        }

    def get_absolute_url(self):
        """Returns the URL to access a particular measurement instance."""
        return reverse("aero:measurement-detail", args=[str(self.id)])
