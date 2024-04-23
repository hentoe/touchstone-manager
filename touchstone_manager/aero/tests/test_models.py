import pytest
from django.utils import timezone

from touchstone_manager.aero.models import Measurement
from touchstone_manager.aero.tests.factories import MaterialFactory
from touchstone_manager.aero.tests.factories import MaterialSampleFactory
from touchstone_manager.aero.tests.factories import MeasurementFactory

# Constants
EXPECTED_SAMPLE_NUMBER = 30
EXPECTED_THICKNESS = 5
EXPECTED_WEIGHT = 38.4
EXPECTED_INFILTRATIONS = 5
EXPECTED_MEAN_S21 = -3.4


@pytest.mark.django_db()
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


@pytest.mark.django_db()
def test_material_str():
    """Test Material object str representation."""
    material = MaterialFactory.create(
        name="Graphene",
        short_name="Gr",
        description="A single layer of carbon atoms.",
    )
    assert str(material) == "Graphene"


@pytest.mark.django_db()
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


@pytest.mark.django_db()
def test_create_material_sample_str():
    """Test MaterialSample object str representation."""
    sample = MaterialSampleFactory.create(
        name="030_FE_aero_4i_5mm_43k4mg",
    )
    assert str(sample) == "030_FE_aero_4i_5mm_43k4mg"


@pytest.mark.django_db()
def test_create_measurement():
    """Test creation of Measurement object."""
    sample = MaterialSampleFactory.create()
    measurement = Measurement.objects.create(
        aero_material=sample,
        measurement_date=timezone.now().date(),
        mean_s21=EXPECTED_MEAN_S21,
    )
    assert measurement.aero_material == sample
    assert measurement.mean_s21 == EXPECTED_MEAN_S21


@pytest.mark.django_db()
def test_measurement_str():
    sample = MaterialSampleFactory()
    measurement_date = timezone.now().date()
    measurement = MeasurementFactory.create(
        measurement_date=measurement_date,
        aero_material=sample,
    )
    assert str(measurement) == f"{sample} on {measurement_date}"
