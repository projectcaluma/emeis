from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string


class DefaultConfig(AppConfig):
    name = "emeis.core"

    def ready(self):
        from .models import VisibilityMixin

        # to avoid recursive import error, load extension classes
        # only once the app is ready
        VisibilityMixin.visibility_classes = [
            import_string(cls) for cls in settings.VISIBILITY_CLASSES
        ]
