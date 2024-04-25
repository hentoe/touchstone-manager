import logging

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def calculate_mean_s21(measurement_id):
    from skrf import Network

    from .models import Measurement

    try:
        measurement = Measurement.objects.get(id=measurement_id)
    except ObjectDoesNotExist:
        logger.exception("Measurement with id %s does not exist.", measurement_id)
        return

    try:
        network = Network(measurement.measurement_file.path)
        s21 = network.s21.s_db
        measurement.mean_s21 = s21.mean()
        measurement.is_processed = True
        measurement.save()
        logger.info(
            "Successfully calculated mean S21 for measurement id %s.",
            measurement_id,
        )
    except Exception:
        logger.exception(
            "Failed to process the measurement file for id %s.",
            measurement_id,
        )
