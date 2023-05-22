from django.db.models import Model, PROTECT, OneToOneField, CharField
from analysis.models.reference_value.Code import Code
from django.urls import reverse


class RiskProfile(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_risk_profile_code)
    name = CharField(max_length=256)

    def __str__(self):
        return f"{self.code} {self.name}"
    
    @staticmethod
    def type_string():
        return "Risk profile"

    def get_absolute_url(self):
        return reverse("risk-profile-detail", args=[str(self.code)])

    def get_base_fields(self):
        return [
            ("Name", "", self.name),
        ]

    def get_fields(self):
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields