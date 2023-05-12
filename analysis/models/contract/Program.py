from analysis.models.reference_value.Company import Company
from analysis.models.reference_value.Currency import Currency
from analysis.models.reference_value.Code import Code
from analysis.models.reference_value.Classification import Classification
from django.db.models import PROTECT, DateField, ForeignKey, Model, OneToOneField
from django.urls import reverse


class Program(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_program_code)
    insured = ForeignKey(Company, on_delete=PROTECT)
    currency = ForeignKey(Currency, on_delete=PROTECT)
    line_of_business = ForeignKey(Classification, on_delete=PROTECT)
    start_date = DateField()
    end_date = DateField()

    @staticmethod
    def type_string():
        return "Program"

    def get_absolute_url(self):
        return reverse("program-detail", args=[str(self.pk)])

    def __repr__(self) -> str:
        return f"{self.code} {self.insured}"

    def __str__(self) -> str:
        return self.__repr__()
    
    def descritpion_field(self, has_link:bool):
        if has_link:
            return ("Code", self.get_absolute_url(), self.code)
        return ("Code", "", self.code)

    def get_base_fields(self):
        return [
            ("Insured", self.insured.get_absolute_url(), self.insured),
            ("Start date", "", self.start_date),
            ("End date", "", self.end_date),
            ("Currency", "", self.currency),
            ("Nr of contracts", "", self.basecontract_set.all().count()), # type: ignore
        ]

    def get_fields(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        contracts = [
            (
                "",
                contract.get_absolute_url(),
                f"{contract.code} - {contract.coverage.type_name()}",
            )
            for contract in self.basecontract_set.all() # type: ignore
        ]
        fields.extend(contracts)
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields
