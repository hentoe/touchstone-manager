import pytest
from django.utils import timezone

from touchstone_manager.aero.models import Material
from touchstone_manager.aero.models import MaterialSample
from touchstone_manager.aero.models import Measurement

# Constants
EXPECTED_SAMPLE_NUMBER = 30
EXPECTED_THICKNESS = 5
EXPECTED_WEIGHT = 38.4
EXPECTED_INFILTRATIONS = 5
EXPECTED_MEAN_S21 = -3.4


@pytest.mark.django_db()
def test_create_material():
    """Test creation of Material object."""
    material = Material.objects.create(
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
    material = Material.objects.create(
        name="Graphene",
        short_name="Gr",
        description="A single layer of carbon atoms.",
    )
    assert str(material) == "Graphene"


@pytest.mark.django_db()
def test_create_material_sample():
    """Test creation of MaterialSample object."""
    material = Material.objects.create(name="Iron", short_name="FE")
    sample = MaterialSample.objects.create(
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
    material = Material.objects.create(name="Iron", short_name="FE")
    sample = MaterialSample.objects.create(
        name="030_FE_aero_4i_5mm_43k4mg",
        sample_number=EXPECTED_SAMPLE_NUMBER,
        material=material,
        thickness=EXPECTED_THICKNESS,
        weight=EXPECTED_WEIGHT,
        infiltrations=EXPECTED_INFILTRATIONS,
    )
    assert str(sample) == "030_FE_aero_4i_5mm_43k4mg"


@pytest.mark.django_db()
def test_create_measurement():
    """Test creation of Measurement object."""
    material = Material.objects.create(name="Fiber Glass", short_name="FG")
    sample = MaterialSample.objects.create(
        name="023_FG_1mm_100mg",
        sample_number=1,
        material=material,
        thickness=1.0,
        weight=100.0,
        infiltrations=0,
    )
    measurement = Measurement.objects.create(
        aero_material=sample,
        measurement_date=timezone.now().date(),
        mean_s21=EXPECTED_MEAN_S21,
    )
    assert measurement.aero_material == sample
    assert measurement.mean_s21 == EXPECTED_MEAN_S21


@pytest.mark.django_db()
def test_measurement_str():
    material = Material.objects.create(name="Fiber Glass", short_name="FG")
    sample = MaterialSample.objects.create(
        name="023_FG_1mm_100mg",
        sample_number=1,
        material=material,
        thickness=1.0,
        weight=100.0,
        infiltrations=0,
    )
    measurement_date = timezone.now().date()
    measurement = Measurement.objects.create(
        aero_material=sample,
        measurement_date=measurement_date,
        mean_s21=-10.5,
    )
    assert str(measurement) == f"{sample} on {measurement_date}"
