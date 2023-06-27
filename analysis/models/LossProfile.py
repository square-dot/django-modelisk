from typing import Any
from django.db.models import Model, PROTECT, OneToOneField, CharField, PositiveIntegerField
from analysis.models.reference_value.Code import Code
from django.urls import reverse


class LossProfile(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_loss_profile_code)
    name = CharField(max_length=256)
    period_length = PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.code} {self.name}"
    
    @staticmethod
    def type_string():
        return "Loss profile"

    def get_absolute_url(self):
        return reverse("loss-profile-detail", args=[str(self.code)])

    def get_base_fields(self) -> list[tuple[str, str, Any]]:
        return [
            ("Name", "", self.name),
        ]

    def get_fields_for_detail(self) -> list[tuple[str, str, Any]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        for risk in self.loss_set.all(): # type: ignore
            fields.append(("Loss", "", risk))
        return fields

    def get_fields_for_list(self) -> list[tuple[str, str, Any]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields