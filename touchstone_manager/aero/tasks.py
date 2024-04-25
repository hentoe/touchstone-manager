import logging

from celery import shared_task

from .models import Measurement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def process_measurement_file(measurement_id):
    from skrf import Network

    try:
        measurement = Measurement.objects.get(pk=measurement_id)
        if measurement.measurement_file:
            network = Network(measurement.measurement_file.path)
            s21 = network.s21.s_db
            measurement.mean_s21 = s21.mean()
            measurement.save()
            logger.info(
                "Processed measurement file and updated mean S21 for %s.",
                measurement_id,
            )

    except Measurement.DoesNotExist:
        logger.exception("Measurement with id %s does not exist.", measurement_id)

    except Exception:
        logger.exception(
            "Error processing measurement file for id %s",
            measurement_id,
        )
