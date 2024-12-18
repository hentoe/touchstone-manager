import zipfile
from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.edit import FormView

from .forms import MaterialSampleFilterForm
from .forms import MeasurementFilterForm
from .forms import MeasurementSelectionForm
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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(sample_count=Count("materialsample"))
        ordering = self.request.GET.get("ordering", "name")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(short_name__icontains=query)
                | Q(description__icontains=query),
            )

        if ordering:
            fields = [field.strip() for field in ordering.split(",")]
            if "materialsample" in fields:
                fields.remove("materialsample")
                fields.append("sample_count")
            if "-materialsample" in fields:
                fields.remove("-materialsample")
                fields.append("-sample_count")
            queryset = queryset.order_by(*fields)
        return queryset


class MaterialSampleDetailView(LoginRequiredMixin, DetailView):
    """Show MaterialSample Details"""

    model = MaterialSample


class MaterialSampleListView(LoginRequiredMixin, ListView):
    """List all MaterialSample"""

    model = MaterialSample

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(measurement_count=Count("measurement"))
        ordering = self.request.GET.get("ordering", "sample_number")

        form = self.get_form()
        if not form.is_valid():
            return MaterialSample.objects.all()

        queryset = self.filter_by_form_fields(queryset, form)

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(material__name__icontains=query)
                | Q(thickness__icontains=query)
                | Q(infiltrations__icontains=query)
                | Q(weight__icontains=query),
            )

        if ordering:
            fields = [field.strip() for field in ordering.split(",")]
            if "measurement" in fields:
                fields.remove("measurement")
                fields.append("measurement_count")
            if "-measurement" in fields:
                fields.remove("-measurement")
                fields.append("-measurement_count")
            queryset = queryset.order_by(*fields)

        return queryset

    def get_form(self):
        return MaterialSampleFilterForm(self.request.GET or None)

    def filter_by_form_fields(self, queryset, form):
        if form.cleaned_data.get("material"):
            material_ids = form.cleaned_data["material"]
            queryset = queryset.filter(material__id__in=material_ids)

        if form.cleaned_data.get("thickness_from"):
            queryset = queryset.filter(
                thickness__gte=form.cleaned_data["thickness_from"],
            )
        if form.cleaned_data.get("thickness_to"):
            queryset = queryset.filter(
                thickness__lte=form.cleaned_data["thickness_to"],
            )
        if form.cleaned_data.get("weight_from"):
            queryset = queryset.filter(
                weight__gte=form.cleaned_data["weight_from"],
            )
        if form.cleaned_data.get("weight_to"):
            queryset = queryset.filter(
                weight__lte=form.cleaned_data["weight_to"],
            )
        if form.cleaned_data.get("infiltrations_from"):
            queryset = queryset.filter(
                infiltrations__gte=form.cleaned_data["infiltrations_from"],
            )
        if form.cleaned_data.get("infiltrations_to"):
            queryset = queryset.filter(
                infiltrations__lte=form.cleaned_data["infiltrations_to"],
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.get_form()
        return context


class MaterialSampleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
    success_message = _("Sample created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create New Sample")
        return context


class MaterialSampleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
    success_message = _("Sample updated successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update Sample")
        return context


class MaterialSampleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = MaterialSample
    success_url = reverse_lazy("aero:samples")
    template_name = "aero/material_confirm_delete.html"
    success_message = _("Sample deleted successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Confirm delete"
        return context


class MeasurementListView(LoginRequiredMixin, ListView):
    """List all Measurements"""

    model = Measurement

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("aero_material", "aero_material__material")
        )
        ordering = self.request.GET.get("ordering", "aero_material__sample_number")

        form = self.get_form()
        if form.is_valid():
            queryset = self.filter_by_form_fields(queryset, form)

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(aero_material__name__icontains=query)
                | Q(mean_s21__icontains=query)
                | Q(measurement_date__icontains=query),
            )

        if ordering:
            fields = [field.strip() for field in ordering.split(",")]
            queryset = queryset.order_by(*fields)

        return queryset

    def get_form(self):
        return MeasurementFilterForm(self.request.GET or None)

    def filter_by_form_fields(self, queryset, form):
        if form.cleaned_data.get("material"):
            material_ids = form.cleaned_data["material"]
            queryset = queryset.filter(aero_material__material__id__in=material_ids)

        if form.cleaned_data.get("mean_s21_from"):
            queryset = queryset.filter(mean_s21__gte=form.cleaned_data["mean_s21_from"])

        if form.cleaned_data.get("mean_s21_to"):
            queryset = queryset.filter(mean_s21__lte=form.cleaned_data["mean_s21_to"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.get_form()
        return context


class MeasurementDetailView(LoginRequiredMixin, DetailView):
    """Show Measurement Details"""

    model = Measurement


class MeasurementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create Measurement instance"""

    model = Measurement
    fields = [
        "aero_material",
        "measurement_file",
        "measurement_date",
    ]
    success_message = _("Measurement created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create New Measurement")
        return context


class MeasurementUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update Measurement instance"""

    model = Measurement
    fields = [
        "aero_material",
        "measurement_file",
    ]
    success_message = _("Measurement updated successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update Measurement")
        return context


class MeasurementDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Measurement
    success_url = reverse_lazy("aero:materials")
    template_name = "aero/material_confirm_delete.html"
    success_message = _("Measurement deleted successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Confirm delete"
        return context


class MaterialCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create Material Instance"""

    model = Material
    fields = ["name", "short_name", "description"]
    success_url = reverse_lazy("aero:materials")
    success_message = _("Material created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create New Material")
        return context


class MaterialUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update Material Instance"""

    model = Material
    fields = ["name", "short_name", "description"]
    success_url = reverse_lazy("aero:materials")
    success_message = _("Material updated successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update Material")
        return context


class MaterialDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Material
    success_url = reverse_lazy("aero:materials")
    success_message = _("Material deleted successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Confirm delete"
        return context


class MeasurementSelectionView(LoginRequiredMixin, FormView):
    template_name = "aero/measurement_download.html"
    form_class = MeasurementSelectionForm
    success_url = reverse_lazy("aero:measurements")

    def form_valid(self, form):
        selected_measurements = form.cleaned_data["measurement_ids"]
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="measurements.zip"'

        with zipfile.ZipFile(response, "w") as zip_file:
            for measurement in selected_measurements:
                file_path = measurement.measurement_file.path
                zip_file.write(file_path, Path(file_path).name)

        return response


material_create_view = MaterialCreateView.as_view()
material_detail_view = MaterialDetailView.as_view()
material_list_view = MaterialListView.as_view()
material_update_view = MaterialUpdateView.as_view()
material_delete_view = MaterialDeleteView.as_view()
material_sample_create_view = MaterialSampleCreateView.as_view()
material_sample_detail_view = MaterialSampleDetailView.as_view()
material_sample_list_view = MaterialSampleListView.as_view()
material_sample_update_view = MaterialSampleUpdateView.as_view()
material_sample_delete_view = MaterialSampleDeleteView.as_view()
measurement_create_view = MeasurementCreateView.as_view()
measurement_detail_view = MeasurementDetailView.as_view()
measurement_list_view = MeasurementListView.as_view()
measurement_update_view = MeasurementUpdateView.as_view()
measurement_delete_view = MeasurementDeleteView.as_view()
measurement_selection_view = MeasurementSelectionView.as_view()
