from django.urls import path

from .views import material_list_view

app_name = "aero"
urlpatterns = [
    path("materials/", view=material_list_view, name="materials"),
]
