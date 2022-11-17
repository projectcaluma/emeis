import mptt
import mptt.managers
from django.conf import settings
from django.utils import translation


def rebuild_mptt_model(model):
    """
    Rebuild an mptt model.

    This is used in migrations that work with data from mptt models.
    """
    manager = mptt.managers.TreeManager()
    manager.model = model
    mptt.register(model)
    manager.contribute_to_class(model, "objects")
    manager.rebuild()


def forced_or_current_lang(model_name):
    """Return the currently to-be-used language for the given model.

    If no monolingual mode is forced for the given model, this will
    return the currently active language as per Django (requested from
    client). However if the model is forced into monolingual mode,
    that language will be returned instead.

    """
    return settings.EMEIS_FORCE_MODEL_LOCALE.get(
        model_name.lower(), translation.get_language()
    )
