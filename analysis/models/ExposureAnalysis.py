from analysis.models.InflationPattern import InflationPattern
from analysis.models.contract.Program import Program
from analysis.models.RiskProfile import RiskProfile
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
    creation_date = DateTimeField(default=datetime.now)
    last_modified = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.code} {self.name}"

    @staticmethod
    def type_string():
        return "Analysis"
    
    def get_base_fields(self):
        return [
            ("Name", "", self.name),
            ("Program", self.program.get_absolute_url(), self.program),
        ]
    
    def get_fields(self):
        fields = self.get_base_fields()
        fields.insert(0, ("Code", "", self.code))
        for ld in self.probabilitydistribution_set.filter(is_total_distribution=False): # type: ignore
            fields.append(("Distribution", "", ld))
        if self.has_total_distribution():
            fields.append(("Total distribution", "", self.probabilitydistribution_set.get(is_total_distribution=True))) # type: ignore
        return fields
    
    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields

    def get_absolute_url(self):
        return reverse("exposure-analysis-detail", args=[str(self.code)])
    
    def has_total_distribution(self) -> bool:
        return any(self.probabilitydistribution_set.filter(is_total_distribution=True)) # type: ignore
    

