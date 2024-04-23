from django.urls import path

from .views import material_detail_view
from .views import material_list_view

app_name = "aero"
urlpatterns = [
    path("materials/", view=material_list_view, name="materials"),
    path("materials/<int:pk>", view=material_detail_view, name="material-detail"),
]
