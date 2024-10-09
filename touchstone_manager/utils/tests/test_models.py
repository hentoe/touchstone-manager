import pytest
from django.utils import timezone


@pytest.mark.django_db
def test_timestamped_model_creation(create_test_model):
    """Test the automatic setting of created and modified fields upon creation."""
    model_instance = create_test_model
    assert model_instance.created is not None
    assert model_instance.modified is not None

    max_delta = timezone.timedelta(seconds=1)  # Allow up to 1 second difference
    assert abs(model_instance.created - model_instance.modified) <= max_delta
