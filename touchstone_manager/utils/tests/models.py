from django.db import models

from touchstone_manager.utils.models import TimeStampedModel


class TimeStampedTestModel(TimeStampedModel):
    name = models.CharField(max_length=100)
