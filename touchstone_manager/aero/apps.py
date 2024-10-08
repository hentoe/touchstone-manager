from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AeroConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "touchstone_manager.aero"
    verbose_name = _("Aero")

    def ready(self):
        import touchstone_manager.aero.signals  # noqa: F401
