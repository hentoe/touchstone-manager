from django.urls import path

from .views import MaterialCreateView
from .views import MaterialDeleteView
from .views import MaterialUpdateView
from .views import material_detail_view
from .views import material_list_view
from .views import material_sample_detail_view
from .views import material_sample_list_view
from .views import measurement_detail_view
from .views import measurement_list_view

app_name = "aero"
urlpatterns = [
    path("materials/", view=material_list_view, name="materials"),
    path(
        "materials/create/",
        view=MaterialCreateView.as_view(),
        name="material-create",
    ),
    path("materials/<int:pk>/", view=material_detail_view, name="material-detail"),
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
    path("samples/", view=material_sample_list_view, name="samples"),
    path("samples/<int:pk>/", view=material_sample_detail_view, name="sample-detail"),
    path("measurements/", view=measurement_list_view, name="measurements"),
    path(
        "measurements/<int:pk>/",
        view=measurement_detail_view,
        name="measurement-detail",
    ),
]
