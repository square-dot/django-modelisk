from typing import Any
from analysis.models.InflationPattern import InflationPattern
from analysis.models.contract.Program import Program
from analysis.models.RiskProfile import RiskProfile
from analysis.models.RiskProfileModel import RiskProfileModel
from analysis.models.reference_value.Code import Code
from django.db.models import PROTECT, CharField, ForeignKey, Model, OneToOneField, DateTimeField
from django.urls import reverse
from datetime import datetime


class ExposureAnalysis(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_analysis_code)
    name = CharField(max_length=256)
    inflation_pattern = ForeignKey(InflationPattern, on_delete=PROTECT, null=True)
    program = ForeignKey(Program, on_delete=PROTECT, null=True)
    risk_profile = ForeignKey(RiskProfile, on_delete=PROTECT, null=True)
    risk_profile_model = ForeignKey(RiskProfileModel, on_delete=PROTECT, null=True)
    creation_date = DateTimeField(default=datetime.now)
    last_modified = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.code} {self.name}"

    @staticmethod
    def type_string():
        return "Analysis"
    
    def get_absolute_url(self):
        return reverse("exposure-analysis-detail", args=[str(self.code)])
    
    def get_base_fields(self) -> list[tuple[str, str, Any]]:
        return [
            ("Name", "", self.name),
            ("Program", "" if self.program is None else self.program.get_absolute_url(), self.program),
        ]
    
    def get_fields_for_detail(self) -> list[tuple[str, str, Any]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        if self.program is not None:
            fields.append(("Program", self.program.get_absolute_url(), self.program))
        else:
            fields.append(("Program", "", ""))
        return fields
    
    def get_fields_for_list(self) -> list[tuple[str, str, Any]]:
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields

    def has_total_distribution(self) -> bool:
        return any(self.probabilitydistribution_set.filter(is_total_distribution=True)) # type: ignore
    

