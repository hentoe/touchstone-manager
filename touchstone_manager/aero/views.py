from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Material
from .models import MaterialSample
from .models import Measurement


class MaterialDetailView(LoginRequiredMixin, DetailView):
    """Show Material Details"""

    model = Material


material_detail_view = MaterialDetailView.as_view()


class MaterialListView(LoginRequiredMixin, ListView):
    """List all Materials"""

    model = Material


material_list_view = MaterialListView.as_view()


class MaterialSampleDetailView(LoginRequiredMixin, DetailView):
    """Show MaterialSample Details"""

    model = MaterialSample


material_sample_detail_view = MaterialSampleDetailView.as_view()


class MaterialSampleListView(LoginRequiredMixin, ListView):
    """List all MaterialSample"""

    model = MaterialSample


material_sample_list_view = MaterialSampleListView.as_view()


class MeasurementListView(LoginRequiredMixin, ListView):
    """List all Measurements"""

    model = Measurement


measurement_list_view = MeasurementListView.as_view()


class MeasurementDetailView(LoginRequiredMixin, DetailView):
    """Show Measurement Details"""

    model = Measurement


measurement_detail_view = MeasurementDetailView.as_view()
