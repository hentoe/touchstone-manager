import pytest

from touchstone_manager.users.models import User
from touchstone_manager.users.tests.factories import UserFactory
from touchstone_manager.utils.tests.models import TimeStampedTestModel


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def create_test_model(db):
    """Fixture to create a test model instance."""
    return TimeStampedTestModel.objects.create(name="Test")
