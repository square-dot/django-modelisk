from django.db.models import (
    Model,
    PROTECT,
    FloatField,
    ForeignKey,
    CharField,
    PositiveIntegerField,
)
from analysis.models.RiskProfile import RiskProfile


class Risk(Model):
    risk_profile = ForeignKey(RiskProfile, on_delete=PROTECT)
    name = CharField(max_length=256)
    quantity = PositiveIntegerField(default=1)
    expected_maximal_loss = FloatField()
    expected_average_loss = FloatField()
    tag_1 = CharField(max_length=256)
    tag_2 = CharField(max_length=256)
    tag_3 = CharField(max_length=256)

    def __str__(self):
        s = f"quantity: {self.quantity}, max loos: {self.expected_maximal_loss},\
                avg loss: {self.expected_average_loss}, tag1: {self.tag_1}, tag2: {self.tag_2}, tag3: {self.tag_3}"
        if self.name != "":
            return f"{self.name} {s}"
        return s
