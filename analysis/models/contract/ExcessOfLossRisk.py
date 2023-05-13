from analysis.models.contract.BaseContract import BaseExcessOfLoss
from django.db.models import FloatField
from django.urls import reverse


class ExcessOfLossRisk(BaseExcessOfLoss):
    risk_retention = FloatField(null=True, default=None)
    risk_limit = FloatField(null=True, default=None)
    aggregate_retention = FloatField(null=True, default=None)
    aggregate_limit = FloatField(null=True, default=None)

    def type_string(self) -> str:
        return "Excess Of Loss Risk"

    def get_absolute_url(self) -> str:
        return reverse("xl-risk", args=[str(self.pk)])

    def limit_retention_string(self) -> str:
        if self.risk_retention is not None:
            return "risk retention {:.0f}".format(self.risk_retention)
        return "no risk retention"

    def __repr__(self):
        return f"{self.code}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str, str]]:
        l = self.get_base_fields()
        l.insert(0, ("Code", "", self.code))
        if self.risk_retention is not None:
            l.append(("Risk retention", "", "{:_}".format(self.risk_retention)))
        if self.risk_limit is not None:
            l.append(("Risk limit", "", "{:_}".format(self.risk_limit)))
        if self.aggregate_retention is not None:
            l.append(("Aggregate retention", "", "{:_}".format(self.aggregate_retention)))
        if self.aggregate_limit is not None:
            l.append(("Aggregate limit", "", "{:_}".format(self.aggregate_limit)))
        for reinstatement in self.reinstatement_set.all():
            l.append((f"Reinstatement {reinstatement.nr}", "", "Size {:.0f}% - Cost {:.0f}%".format(reinstatement.size * 100, reinstatement.cost * 100)))
        return l
    