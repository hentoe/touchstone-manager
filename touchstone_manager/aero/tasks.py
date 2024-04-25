from celery import shared_task


@shared_task
def calculate_mean_s21(measurement_id):
    from skrf import Network

    from .models import Measurement

    measurement = Measurement.objects.get(id=measurement_id)
    network = Network(measurement.measurement_file)
    s21 = network.s21.s_db
    measurement.mean_s21 = s21.mean()
    measurement.save()
