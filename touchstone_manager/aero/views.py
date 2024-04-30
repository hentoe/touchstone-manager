from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from .models import Material
from .models import MaterialSample
from .models import Measurement


class HomeView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ["pages/home.html"]

        return ["pages/landing.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["materials"] = Material.objects.all().count()
            context["samples"] = MaterialSample.objects.all().count()
            context["measurements"] = Measurement.objects.all().count()
        return context


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


class MaterialCreateView(LoginRequiredMixin, CreateView):
    """Create Material Instance"""

    model = Material
    fields = ["name", "short_name", "description"]
    success_url = reverse_lazy("aero:materials")
