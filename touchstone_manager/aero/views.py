from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Material


class MaterialDetailView(LoginRequiredMixin, DetailView):
    """Show Material Details"""

    model = Material


material_detail_view = MaterialDetailView.as_view()


class MaterialListView(LoginRequiredMixin, ListView):
    """List all Materials"""

    model = Material


material_list_view = MaterialListView.as_view()
