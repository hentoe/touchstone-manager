from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

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


class MaterialListView(LoginRequiredMixin, ListView):
    """List all Materials"""

    model = Material


class MaterialSampleDetailView(LoginRequiredMixin, DetailView):
    """Show MaterialSample Details"""

    model = MaterialSample


class MaterialSampleListView(LoginRequiredMixin, ListView):
    """List all MaterialSample"""

    model = MaterialSample


class MaterialSampleCreateView(LoginRequiredMixin, CreateView):
    """Create MaterialSample instance"""

    model = MaterialSample
    fields = [
        "name",
        "material",
        "sample_number",
        "thickness",
        "weight",
        "infiltrations",
    ]
    template_name = "aero/material_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create New Sample")
        return context


class MaterialSampleUpdateView(LoginRequiredMixin, UpdateView):
    """Update MaterialSample instance"""

    model = MaterialSample
    fields = [
        "name",
        "material",
        "sample_number",
        "thickness",
        "weight",
        "infiltrations",
    ]
    template_name = "aero/material_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update Sample")
        return context


class MaterialSampleDeleteView(LoginRequiredMixin, DeleteView):
    model = MaterialSample
    success_url = reverse_lazy("aero:samples")
    template_name = "aero/material_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Confirm delete"
        return context


class MeasurementListView(LoginRequiredMixin, ListView):
    """List all Measurements"""

    model = Measurement


class MeasurementDetailView(LoginRequiredMixin, DetailView):
    """Show Measurement Details"""

    model = Measurement


class MaterialCreateView(LoginRequiredMixin, CreateView):
    """Create Material Instance"""

    model = Material
    fields = ["name", "short_name", "description"]
    success_url = reverse_lazy("aero:materials")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create New Material")
        return context


class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    """Update Material Instance"""

    model = Material
    fields = ["name", "short_name", "description"]
    success_url = reverse_lazy("aero:materials")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update Material")
        return context


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy("aero:materials")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Confirm delete"
        return context
