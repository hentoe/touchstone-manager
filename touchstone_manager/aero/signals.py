from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Measurement
from .tasks import calculate_mean_s21


@receiver(post_save, sender=Measurement)
def trigger_s21_calculation(sender, instance, created, **kwargs):
    if (
        instance.measurement_file
    ):  # Ensuring there is a file associated with the instance
        calculate_mean_s21.delay(instance.id)
