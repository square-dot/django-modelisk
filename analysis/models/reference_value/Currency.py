from django.core.validators import RegexValidator
from django.db.models import CharField, Model


class Currency(Model):
    iso_code_3 = CharField(
        max_length=3,
        validators=[RegexValidator(r"^\w{3}$", "Must be exactly 3 characters")],
        unique=True,
    )
    name = CharField(max_length=256, default="no_name")

    def __repr__(self) -> str:
        return self.iso_code_3

    def __str__(self) -> str:
        return self.__repr__()