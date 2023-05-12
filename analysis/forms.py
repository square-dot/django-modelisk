from django import forms

from analysis.models.contract.ExcessOfLossRisk import ExcessOfLossRisk
from analysis.models.contract.Premium import Premium
from analysis.models.contract.QuotaShare import QuotaShare


class ContractForm(forms.Form):
    insured = forms.CharField()
    contract_type = forms.Select(choices=[('risk', 'Risk XL'), ('event', 'Event XL'), ('share', 'QS')])
    share = forms.FloatField()
    limit = forms.FloatField()
    retention = forms.FloatField()
    aggregate_limit = forms.FloatField()
    reinstatements = forms.FloatField()


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
    function = forms.CharField(max_length=256, widget=forms.HiddenInput())

