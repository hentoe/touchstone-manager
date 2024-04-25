from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Measurement
from .tasks import process_measurement_file


@receiver(post_save, sender=Measurement)
def trigger_file_processing(sender, instance, created, **kwargs):
    # Trigger task only if the FileField is updated or on creation of a new instance
    if created or "measurement_file" in kwargs.get("update_fields", []):
        process_measurement_file.delay(instance.pk)
