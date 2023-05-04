from analysis.models.Company import Company
from analysis.models.Currency import Currency
from analysis.models.Code import Code
from django.db.models import PROTECT, DateField, ForeignKey, Model, OneToOneField
from django.urls import reverse


class Program(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_program_code)
    insured = ForeignKey(Company, on_delete=PROTECT)
    currency = ForeignKey(Currency, on_delete=PROTECT)
    start_date = DateField()
    end_date = DateField()

    def get_absolute_url(self):
        return reverse("program-detail", args=[str(self.pk)])
    
    def __repr__(self) -> str:
        return f"{self.code} {self.insured}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str]]:
        contracts = [
            ("", f"{contract.code} - {contract.coverage.type_name()}")
            for contract in self.contract_set.all()
        ]

        fields = [
            ("ID", self.code),
            ("Insured", self.insured),
            ("Start date", self.start_date),
            ("End date", self.end_date),
            ("Currency", self.currency),
            ("Contracts", self.contract_set.all().count()),
        ]
        fields.extend(contracts)
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = [
            ("ID", self.get_absolute_url(), self.code),
            ("Insured", self.insured.get_absolute_url(), self.insured),
            ("Start date", "", self.start_date),
            ("End date", "", self.end_date),
            ("Currency", "", self.currency),
            ("Nr of contracts", "", self.contract_set.all().count()),
        ]
        return fields