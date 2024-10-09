from unittest.mock import patch

import pytest
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from touchstone_manager.aero.models import Material
from touchstone_manager.aero.models import MaterialSample
from touchstone_manager.aero.tests.factories import MaterialFactory
from touchstone_manager.aero.tests.factories import MaterialSampleFactory
from touchstone_manager.aero.tests.factories import MeasurementFactory

# Constants
EXPECTED_SAMPLE_NUMBER = 30
EXPECTED_THICKNESS = 5
EXPECTED_WEIGHT = 38.4
EXPECTED_INFILTRATIONS = 5
EXPECTED_MEAN_S21 = -3.4


@pytest.mark.django_db
def test_create_material():
    """Test creation of Material object."""
    material = MaterialFactory.create(
        name="Graphene",
        short_name="eG",
        description="exfoliated Graphene",
    )
    assert material.name == "Graphene"
    assert material.short_name == "eG"
    assert material.description == "exfoliated Graphene"


@pytest.mark.django_db
def test_material_str():
    """Test Material object str representation."""
    material = MaterialFactory.create(
        name="Graphene",
        short_name="Gr",
        description="A single layer of carbon atoms.",
    )
    assert str(material) == "Graphene"


@pytest.mark.django_db
def test_create_material_sample():
    """Test creation of MaterialSample object."""
    material = MaterialFactory.create()
    sample = MaterialSampleFactory.create(
        name="030_FE_aero_4i_5mm_43k4mg",
        sample_number=EXPECTED_SAMPLE_NUMBER,
        material=material,
        thickness=EXPECTED_THICKNESS,
        weight=EXPECTED_WEIGHT,
        infiltrations=EXPECTED_INFILTRATIONS,
    )
    assert sample.name == "030_FE_aero_4i_5mm_43k4mg"
    assert sample.sample_number == EXPECTED_SAMPLE_NUMBER
    assert sample.material == material
    assert sample.thickness == EXPECTED_THICKNESS
    assert sample.weight == EXPECTED_WEIGHT
    assert sample.infiltrations == EXPECTED_INFILTRATIONS


@pytest.mark.django_db
def test_create_material_sample_str():
    """Test MaterialSample object str representation."""
    sample = MaterialSampleFactory.create(
        name="030_FE_aero_4i_5mm_43k4mg",
    )
    assert str(sample) == "030_FE_aero_4i_5mm_43k4mg"


@pytest.mark.django_db
@patch("touchstone_manager.aero.models.Measurement.process_file")
def test_create_measurement(mock_process_file):
    """Test creation of Measurement object."""
    mock_process_file.return_value = None
    sample = MaterialSampleFactory.create()
    measurement = MeasurementFactory.create(
        aero_material=sample,
        measurement_date=timezone.now(),
    )
    assert measurement.aero_material == sample


@pytest.mark.django_db
@patch("touchstone_manager.aero.models.Measurement.process_file")
def test_measurement_str(mock_process_file):
    mock_process_file.return_value = None
    sample = MaterialSampleFactory()
    measurement_date = timezone.now()
    measurement = MeasurementFactory.create(
        measurement_date=measurement_date,
        aero_material=sample,
    )
    assert str(measurement) == _("%(aero_material)s on %(date)s") % {
        "aero_material": measurement.aero_material.name,
        "date": measurement.measurement_date,
    }

    mock_process_file.assert_called_once()


def test_material_get_absolute_url(material: Material):
    base_url = reverse("aero:materials")
    assert material.get_absolute_url() == f"{base_url}{material.pk}/"


def test_material_sample_get_absolute_url(material_sample: MaterialSample):
    base_url = reverse("aero:samples")
    assert material_sample.get_absolute_url() == f"{base_url}{material_sample.pk}/"


@pytest.mark.django_db
@patch("touchstone_manager.aero.models.Measurement.process_file")
def test_measurement_get_absolute_url(mock_process_file):
    mock_process_file.return_value = None
    base_url = reverse("aero:measurements")
    measurement = MeasurementFactory.create()
    assert measurement.get_absolute_url() == f"{base_url}{measurement.pk}/"
