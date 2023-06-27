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
    tags_string = CharField(max_length=1024, default="")

    def tags(self) -> list[str]:
        return self.tags_string.split(" ")

    def __str__(self):
        s = f"quantity: {self.quantity}, max loos: {self.expected_maximal_loss}, avg loss: {self.expected_average_loss}"
        string_of_tags = ", ".join(self.tags())
        s += f", tags: {string_of_tags}"
        if self.name != "":
            return f"{self.name} {s}"
        return s
