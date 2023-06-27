from typing import Any
from django.db.models import Model, PROTECT, CASCADE, FloatField, ForeignKey, OneToOneField, DateTimeField
from analysis.models.reference_value.Code import Code
from analysis.models.reference_value.Currency import Currency
from analysis.models.contract.Premium import Premium
from analysis.models.contract.Program import Program
from analysis.models.contract.Expenses import Expenses
from datetime import datetime
from django.urls import reverse


class Layer(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_layer_code)
    program = ForeignKey(Program, on_delete=CASCADE)
    currency = ForeignKey(Currency, on_delete=PROTECT)
    premium = OneToOneField(Premium, on_delete=PROTECT)
    expenses = OneToOneField(Expenses, on_delete=PROTECT)
    participation = FloatField(help_text="percentage share acquired")
    share = FloatField(default=1)
    event_retention = FloatField(null=True, default=None)
    event_limit = FloatField(null=True, default=None)
    risk_retention = FloatField(null=True, default=None)
    risk_limit = FloatField(null=True, default=None)
    aggregate_retention = FloatField(null=True, default=None)
    aggregate_limit = FloatField(null=True, default=None)
    franchise_deductible = FloatField(null=True, default=0)
    loss_corridors = FloatField(default=0) # this is just a placeholder
    loss_participation_clause = FloatField(default=0) # this is just a placeholder
    creation_date = DateTimeField(default=datetime.now)
    last_modified = DateTimeField(default=datetime.now)

    @staticmethod
    def type_string():
        return "Layer"

    def __repr__(self) -> str:
        return f"{self.type_string()} {self.code}"

    def __str__(self) -> str:
        return self.__repr__()
    
    def get_absolute_url(self):
        return reverse("layer", args=[str(self.code)])

    def get_base_fields(self) -> list[tuple[str, str, Any]]:
        return [
            ("Program", self.program.get_absolute_url(), self.program),
            ("Type", "", self.type_string()),
            ("Premium", "", self.premium.upfront_premium),
            ("Expenses", "", self.expenses.upfront_expenses),
        ]

    def get_fields_for_detail(self) -> list[tuple[str, str, Any]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, Any]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields
