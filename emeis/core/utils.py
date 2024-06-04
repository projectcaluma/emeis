from django.conf import settings
from django.utils import translation


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
