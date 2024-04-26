import factory.django
from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from touchstone_manager.aero.models import Material
from touchstone_manager.aero.models import MaterialSample
from touchstone_manager.aero.models import Measurement


class MaterialFactory(DjangoModelFactory):
    """Factory for Material Model"""

    class Meta:
        model = Material

    name = Faker("word")
    short_name = Faker("word")
    description = Faker("text", max_nb_chars=200)


class MaterialSampleFactory(DjangoModelFactory):
    """Factory for MaterialSample Model"""

    class Meta:
        model = MaterialSample

    name = Faker("word")
    sample_number = Faker("pyint", min_value=0, max_value=10000)
    material = SubFactory(MaterialFactory)
    thickness = Faker("pyfloat", min_value=0, max_value=10)
    weight = Faker("pyfloat", min_value=0, max_value=1000)
    infiltrations = Faker("pyint", min_value=0, max_value=100)


class MeasurementFactory(DjangoModelFactory):
    """Factory for Measurement Model"""

    class Meta:
        model = Measurement

    aero_material = SubFactory(MaterialSampleFactory)
    measurement_date = Faker("date")
    measurement_file = factory.django.FileField()
    mean_s21 = Faker("pyfloat", min_value=-100, max_value=0)
