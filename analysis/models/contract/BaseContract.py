from django.db.models import PROTECT, FloatField, ForeignKey, OneToOneField
from polymorphic.models import PolymorphicModel
from analysis.models.reference_value.Code import Code
from analysis.models.reference_value.Currency import Currency
from analysis.models.contract.Premium import Premium
from analysis.models.contract.Program import Program


class BaseContract(PolymorphicModel):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_contract_code)
    currency = ForeignKey(Currency, on_delete=PROTECT)
    premium = OneToOneField(Premium, on_delete=PROTECT)
    brokerage = FloatField(default=0)
    commission = FloatField(default=0)
    program = ForeignKey(Program, on_delete=PROTECT)
    participation = FloatField(help_text="percentage share acquired")

    @staticmethod
    def type_string():
        return "Contract"

    def __repr__(self) -> str:
        return f"{self.code} {self.type_string()}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_base_fields(self):
        return [
            ("Program", self.program.get_absolute_url(), self.program),
            ("Type", "", self.type_string()),
            ("Premium", "", self.premium.upfront_premium),
            ("Brokerage", "", self.brokerage),
            ("Commission", "", self.commission),
        ]

    def get_fields(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields
    

class BaseExcessOfLoss(BaseContract):
    pass
