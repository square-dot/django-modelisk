from analysis.models.Coverage import Coverage
from django.db.models import FloatField


class ExcessOfLoss(Coverage):
    risk_retention = FloatField(null=True, default=None)
    risk_limit = FloatField(null=True, default=None)
    event_retention = FloatField(null=True, default=None)
    event_limit = FloatField(null=True, default=None)
    aggregate_retention = FloatField(null=True, default=None)
    aggregate_limit = FloatField(null=True, default=None)

    def type_name(self) -> str:
        return "Excess Of Loss"

    def limit_retention_string(self) -> str:
        if self.risk_retention is not None:
            return "risk retention {:.0f}".format(self.risk_retention)
        return "no risk retention"

    def __repr__(self):
        return self.type_name()

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str]]:
        l = []
        if self.risk_retention is not None:
            l.append(("Risk retention", "{:_}".format(self.risk_retention)))
        if self.risk_limit is not None:
            l.append(("Risk limit", "{:_}".format(self.risk_limit)))
        if self.event_retention is not None:
            l.append(("Event retention", "{:_}".format(self.event_retention)))
        if self.event_limit is not None:
            l.append(("Event limit", "{:_}".format(self.event_limit)))
        if self.aggregate_retention is not None:
            l.append(("Aggregate retention", "{:_}".format(self.aggregate_retention)))
        if self.aggregate_limit is not None:
            l.append(("Aggregate limit", "{:_}".format(self.aggregate_limit)))
        return l