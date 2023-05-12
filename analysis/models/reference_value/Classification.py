from django.core.validators import RegexValidator
from django.db.models import CharField, Model


class Classification(Model):
    PROPERTY = "Property"
    CASULATY = "Casualty"
    AGRICULTURE = "Agriculture"
    MOTOR = "Motor"
    LOB_TYPES = (
        (PROPERTY, "Property"),
        (CASULATY, "Casualty"),
        (AGRICULTURE, "Agriculture"),
        (MOTOR, "Motor"),
    )

    name = CharField(choices=LOB_TYPES, max_length=32)

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.__repr__()
