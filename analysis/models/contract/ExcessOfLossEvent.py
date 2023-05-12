from analysis.models.contract.BaseContract import BaseExcessOfLoss
from django.db.models import FloatField
from django.urls import reverse


class ExcessOfLossEvent(BaseExcessOfLoss):
    event_retention = FloatField(null=True, default=None)
    event_limit = FloatField(null=True, default=None)
    aggregate_retention = FloatField(null=True, default=None)
    aggregate_limit = FloatField(null=True, default=None)

    def type_string(self) -> str:
        return "Excess Of Loss"
    
    def get_absolute_url(self) -> str:
        return reverse("xl-event", args=[str(self.pk)])

    def limit_retention_string(self) -> str:
        if self.event_retention is not None:
            return "event retention {:.0f}".format(self.risk_retention)
        return "no event retention"

    def __repr__(self):
        return self.type_name()

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str]]:
        l = []
        if self.event_retention is not None:
            l.append(("Event retention", "{:_}".format(self.event_retention)))
        if self.event_limit is not None:
            l.append(("Event limit", "{:_}".format(self.event_limit)))
        if self.aggregate_retention is not None:
            l.append(("Aggregate retention", "{:_}".format(self.aggregate_retention)))
        if self.aggregate_limit is not None:
            l.append(("Aggregate limit", "{:_}".format(self.aggregate_limit)))
        for reinstatement in self.reinstatement_set.all():
            l.append((f"Reinstatement {reinstatement.nr}", "Size {:.0f}% - Cost {:.0f}%".format(reinstatement.size * 100, reinstatement.cost * 100)))
        return l
    