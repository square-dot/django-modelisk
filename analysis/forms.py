from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from analysis.models.reference_value.Company import Company


from analysis.models.contract.ExcessOfLossRisk import ExcessOfLossRisk
from analysis.models.contract.Premium import Premium
from analysis.models.contract.QuotaShare import QuotaShare
from analysis.models.ExposureAnalysis import ExposureAnalysis


class ContractForm(forms.Form):
    insured = forms.ChoiceField(choices=[(c, c.name) for c in Company.objects.order_by("name")])
    contract_type = forms.ChoiceField(widget=forms.RadioSelect, choices=[('risk', 'Risk XL'), ('event', 'Event XL'), ('share', 'QS')])
    participation = forms.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)
    share = forms.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], required=False)
    risk_limit = forms.FloatField(validators=[MinValueValidator(0.0)], required=False)
    risk_retention = forms.FloatField(validators=[MinValueValidator(0.0)], required=False)
    event_limit = forms.FloatField(validators=[MinValueValidator(0.0)], required=False)
    event_retention = forms.FloatField(validators=[MinValueValidator(0.0)], required=False)
    aggregate_limit = forms.FloatField(validators=[MinValueValidator(0.0)], required=False)
    aggregate_retention = forms.FloatField(validators=[MinValueValidator(0.0)], required=False)
    reinstatements = forms.IntegerField(validators=[MinValueValidator(0)], required=False)


class PremiumForm(forms.ModelForm):
    class Meta:
        model = Premium
        fields = '__all__'


class ExcessOfLossRiskForm(forms.ModelForm):
    class Meta:
        model = ExcessOfLossRisk
        fields = '__all__'


class QuotaShareForm(forms.ModelForm):
    class Meta:
        model = QuotaShare
        fields = '__all__'


class CreateConvolution(forms.Form):
    function = forms.CharField(max_length=256, widget=forms.HiddenInput(), initial={"function": "create_convolution"})

class ExposureAnalysisForm(forms.ModelForm):
    class Meta:
        model = ExposureAnalysis
        fields = '__all__'

