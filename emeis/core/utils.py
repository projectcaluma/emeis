import mptt
import mptt.managers


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
