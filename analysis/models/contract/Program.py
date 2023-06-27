from typing import Any
from analysis.models.reference_value.Company import Company
from analysis.models.reference_value.Currency import Currency
from analysis.models.reference_value.Code import Code
from analysis.models.reference_value.Classification import Classification
from django.db.models import PROTECT, DateField, ForeignKey, Model, OneToOneField, DateTimeField
from django.urls import reverse
from datetime import datetime


class Program(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_program_code)
    insured = ForeignKey(Company, on_delete=PROTECT)
    currency = ForeignKey(Currency, on_delete=PROTECT)
    line_of_business = ForeignKey(Classification, on_delete=PROTECT)
    start_date = DateField()
    end_date = DateField()
    creation_date = DateTimeField(default=datetime.now)
    last_modified = DateTimeField(default=datetime.now)

    @staticmethod
    def type_string():
        return "Program"

    def get_absolute_url(self):
        return reverse("program-detail", args=[str(self.code)])

    def __repr__(self) -> str:
        return f"{self.code} {self.insured}"

    def __str__(self) -> str:
        return self.__repr__()
    
    def descritpion_field(self, has_link:bool):
        if has_link:
            return ("Code", self.get_absolute_url(), self.code)
        return ("Code", "", self.code)

    def get_base_fields(self) -> list[tuple[str, str, Any]]:
        return [
            ("Insured", self.insured.get_absolute_url(), self.insured),
            ("Start date", "", self.start_date),
            ("End date", "", self.end_date),
            ("Currency", "", self.currency),
            ("Nr of layers", "", self.layer_set.all().count()), # type: ignore
        ]

    def get_fields_for_detail(self) -> list[tuple[str, str, Any]]: 
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        layers = [
            (
                "",
                layer.get_absolute_url(),
                f"{layer}",
            )
            for layer in self.layer_set.all() # type: ignore
        ]
        fields.extend(layers)
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, Any]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields
