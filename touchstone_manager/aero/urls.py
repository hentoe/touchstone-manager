from django.urls import path

from .views import material_create_view
from .views import material_delete_view
from .views import material_detail_view
from .views import material_list_view
from .views import material_sample_create_view
from .views import material_sample_delete_view
from .views import material_sample_detail_view
from .views import material_sample_list_view
from .views import material_sample_update_view
from .views import material_update_view
from .views import measurement_create_view
from .views import measurement_delete_view
from .views import measurement_detail_view
from .views import measurement_list_view
from .views import measurement_update_view

app_name = "aero"
urlpatterns = [
    path("materials/", view=material_list_view, name="materials"),
    path(
        "materials/create/",
        view=material_create_view,
        name="material-create",
    ),
    path(
        "materials/<int:pk>/",
        view=material_detail_view,
        name="material-detail",
    ),
    path(
        "materials/<int:pk>/update/",
        view=material_update_view,
        name="material-update",
    ),
    path(
        "material/<int:pk>/delete/",
        view=material_delete_view,
        name="material-delete",
    ),
    path("samples/", view=material_sample_list_view, name="samples"),
    path(
        "samples/create/",
        view=material_sample_create_view,
        name="sample-create",
    ),
    path(
        "samples/<int:pk>/",
        view=material_sample_detail_view,
        name="sample-detail",
    ),
    path(
        "samples/<int:pk>/update",
        view=material_sample_update_view,
        name="sample-update",
    ),
    path(
        "samples/<int:pk>/delete",
        view=material_sample_delete_view,
        name="sample-delete",
    ),
    path("measurements/", view=measurement_list_view, name="measurements"),
    path(
        "measurements/create/",
        view=measurement_create_view,
        name="measurement-create",
    ),
    path(
        "measurements/<int:pk>/",
        view=measurement_detail_view,
        name="measurement-detail",
    ),
    path(
        "measurements/<int:pk>/update",
        view=measurement_update_view,
        name="measurement-update",
    ),
    path(
        "measurements/<int:pk>/delete",
        view=measurement_delete_view,
        name="measurement-delete",
    ),
]
