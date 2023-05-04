from analysis.models.Coverage import Coverage
from analysis.models.Currency import Currency
from analysis.models.Expenses import Expenses
from analysis.models.Premium import Premium
from analysis.models.Program import Program
from analysis.models.Code import Code
from django.db.models import PROTECT, ForeignKey, Model, OneToOneField
from django.urls import reverse


class Contract(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_contract_code)
    currency = ForeignKey(Currency, on_delete=PROTECT)
    premium = OneToOneField(Premium, on_delete=PROTECT)
    expenses = OneToOneField(Expenses, on_delete=PROTECT)
    coverage = OneToOneField(Coverage, on_delete=PROTECT)
    program = ForeignKey(Program,on_delete=PROTECT)

    def get_absolute_url(self) -> str:
        return reverse("contract-detail", args=[str(self.pk)])

    def __repr__(self) -> str:
        return f"{self.code} {self.coverage.__repr__()}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str]]:
        fields = [
            ("Code", self.code),
            ("Type", self.coverage.type_name()),
            ("Premium", self.premium.upfront_premium),
            ("Brokerage", self.expenses.upfront_brokerage),
            ("Commission", self.expenses.upfront_commission),
        ]
        fields.extend(self.coverage.get_fields())
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        return [
            ("Code", self.get_absolute_url(), self.code),
            ("Type", "", self.coverage.type_name()),
            ("Premium", "", self.premium.upfront_premium),
            ("Brokerage", "", self.expenses.upfront_brokerage),
            ("Commission", "", self.expenses.upfront_commission),
        ]
