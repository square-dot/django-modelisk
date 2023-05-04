from django.db.models import FloatField
from polymorphic.models import PolymorphicModel


class Coverage(PolymorphicModel):
    participation = FloatField(help_text="percentage share acquired")