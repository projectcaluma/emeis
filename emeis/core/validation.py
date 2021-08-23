from collections import defaultdict
from functools import wraps


def validator_for(model_cls):
    """Decorate custom validator function.

    Decorate your validator methods to tell Emeis which
    model they can be used for.
    """

    def add_validator_decoration(func):
        if hasattr(func, "_emeis_validator_for"):
            func._emeis_validator_for.append(model_cls)
            return func

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        wrapped._emeis_validator_for = [model_cls]

        return wrapped

    return add_validator_decoration


class EmeisBaseValidator:
    """Base class for custom validations.

    Extend this to implement your custom Emeis validators. The validation methods
    will receive the data to be validated, and are expected to return the data back to the caller.

    You can modify the data, or raise a `ValidationError` if needed.

    Example:
    >>> from emeis.core.validation import EmeisBaseValidator, validator_for
    >>> from emeis.core.models import User
    >>> class LowercaseUsername(EmeisBaseValidator):
    ...     @validator_for(User)
    ...     def lowercase_username(self, data):
    ...         data['username'] = data['username'].lower()
    ...         return data
    """

    def __init__(self, context):
        self.context = context


class ValidatorMixin:
    validators = defaultdict(list)

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        for validator_cls, method in self.validators[self.Meta.model]:
            validator = validator_cls(context=self.context)
            validated_data = method(validator, validated_data)
        return validated_data

    @classmethod
    def register_validation_classes(cls, class_list):
        cls.validators = defaultdict(list)

        for validator_cls in class_list:
            for prop in vars(validator_cls).values():
                cls._check_and_register_method(validator_cls, prop)

    @classmethod
    def _check_and_register_method(cls, validator_cls, meth):
        if not hasattr(meth, "_emeis_validator_for"):
            return
        for model in meth._emeis_validator_for:
            cls.validators[model].append((validator_cls, meth))
