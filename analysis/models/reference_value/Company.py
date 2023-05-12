from analysis.models.reference_value.Country import Country
from django.db import models
from django.db.models import PROTECT, CharField, ForeignKey, Model
from django.db.models.functions import Lower
from django.urls import reverse


class Company(Model):
    name = CharField(max_length=256)
    country = ForeignKey(Country, on_delete=PROTECT)
    email = CharField(max_length=256, default="")

    @staticmethod
    def type_string():
        return "Company"

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_absolute_url(self):
        return reverse("company-detail", args=[str(self.pk)])

    def get_base_fields(self):
        return [
            ("Country", "", self.country.name),
            ("E-mail", "", self.email),
        ]

    def get_fields(self) -> list[tuple[str, str, any]]: # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Name", "", self.name))
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, str]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Name", self.get_absolute_url(), self.name))
        return fields

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_lower_company_name")
        ]
