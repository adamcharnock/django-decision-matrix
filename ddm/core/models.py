from django.apps import apps

from ddm.core import abstract_models

__all__ = []


def is_model_registered(app_label, model_name):
    try:
        apps.get_registered_model(app_label, model_name)
    except LookupError:
        return False
    else:
        return True


if not is_model_registered('core', 'Option'):
    class Option(abstract_models.AbstractOption):
        pass

    __all__.append('Option')


if not is_model_registered('core', 'Criterion'):
    class Criterion(abstract_models.AbstractCriterion):
        pass

    __all__.append('Criterion')


if not is_model_registered('core', 'Weight'):
    class Weight(abstract_models.AbstractWeight):
        pass

    __all__.append('Weight')


if not is_model_registered('core', 'Score'):
    class Score(abstract_models.AbstractScore):
        pass

    __all__.append('Score')


if not is_model_registered('core', 'Category'):
    class Category(abstract_models.AbstractCategory):
        pass

    __all__.append('Category')


