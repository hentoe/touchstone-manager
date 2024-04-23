from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Material


class MaterialListView(LoginRequiredMixin, ListView):
    """List all Materials"""

    model = Material


material_list_view = MaterialListView.as_view()
