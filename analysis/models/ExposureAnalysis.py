from analysis.models.InflationPattern import InflationPattern
from analysis.models.Program import Program
from analysis.models.Code import Code
from django.db.models import PROTECT, CharField, ForeignKey, Model, OneToOneField
from django.urls import reverse


class ExposureAnalysis(Model):
    code = OneToOneField(Code, on_delete=PROTECT, default=Code.next_analysis_code)
    name = CharField(max_length=256)
    inflation_pattern = ForeignKey(InflationPattern, on_delete=PROTECT)
    program = ForeignKey(Program, on_delete=PROTECT)

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
        for ld in self.lossdistribution_set.all():
            fields.append(("Distribution", "", ld))
        return fields
    
    def get_fields_for_list(self) -> list[tuple[str, str, any]]:  # type: ignore
        fields = self.get_base_fields()
        fields.insert(0, ("Code", self.get_absolute_url(), self.code))
        return fields

    def get_absolute_url(self):
        return reverse("exposure-analysis-detail", args=[str(self.pk)])
