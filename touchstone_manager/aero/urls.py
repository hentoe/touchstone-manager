from django.urls import path

from .views import MaterialCreateView
from .views import MaterialDeleteView
from .views import MaterialDetailView
from .views import MaterialListView
from .views import MaterialSampleCreateView
from .views import MaterialSampleDeleteView
from .views import MaterialSampleDetailView
from .views import MaterialSampleListView
from .views import MaterialSampleUpdateView
from .views import MaterialUpdateView
from .views import MeasurementDetailView
from .views import MeasurementListView

app_name = "aero"
urlpatterns = [
    path("materials/", view=MaterialListView.as_view(), name="materials"),
    path(
        "materials/create/",
        view=MaterialCreateView.as_view(),
        name="material-create",
    ),
    path(
        "materials/<int:pk>/",
        view=MaterialDetailView.as_view(),
        name="material-detail",
    ),
    path(
        "materials/<int:pk>/update/",
        view=MaterialUpdateView.as_view(),
        name="material-update",
    ),
    path(
        "material/<int:pk>/delete/",
        MaterialDeleteView.as_view(),
        name="material-delete",
    ),
    path("samples/", view=MaterialSampleListView.as_view(), name="samples"),
    path(
        "samples/create/",
        view=MaterialSampleCreateView.as_view(),
        name="sample-create",
    ),
    path(
        "samples/<int:pk>/",
        view=MaterialSampleDetailView.as_view(),
        name="sample-detail",
    ),
    path(
        "samples/<int:pk>/update",
        view=MaterialSampleUpdateView.as_view(),
        name="sample-update",
    ),
    path(
        "samples/<int:pk>/delete",
        view=MaterialSampleDeleteView.as_view(),
        name="sample-delete",
    ),
    path("measurements/", view=MeasurementListView.as_view(), name="measurements"),
    path(
        "measurements/<int:pk>/",
        view=MeasurementDetailView.as_view(),
        name="measurement-detail",
    ),
]
