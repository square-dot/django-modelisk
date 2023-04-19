from django import forms
from .models import Contract, ContractAdminInfo, ExcessOfLossRisk, ExcessOfLossEvent, QuotaShare

class ContractAdminInfoForm(forms.ModelForm):
    class Meta:
        model = ContractAdminInfo
        fields = '__all__'


class ContractForm(forms.Form):
    insured = forms.CharField()
    choice = forms.Select(choices=[('risk', 'Risk XL'), ('event', 'Event XL'), ('share', 'QS')])
    share = forms.FloatField()
    limit = forms.FloatField()
    retention = forms.FloatField()
    aggregate_retention = forms.FloatField()
    reinstatements = forms.FloatField()
    







    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['coverage_info'].widget = forms.Select(choices=[('risk', 'Risk XL'), ('event', 'Event XL'), ('share', 'QS')])

    #     # Create empty forms for each of the related models
    #     self.excess_of_loss_risk_form = ExcessOfLossRiskForm()
    #     self.excess_of_loss_event_form = ExcessOfLossEventForm()
    #     self.quota_share_form = QuotaShareForm()

    def clean(self):
        cleaned_data = super().clean()
        choice = cleaned_data.get('coverage_info')

        # Based on the choice, set the relevant form instance as the active form
        # if choice == 'risk':
        #     self.active_form = self.excess_of_loss_risk_form
        # elif choice == 'event':
        #     self.active_form = self.excess_of_loss_event_form
        # elif choice == 'share':
        #     self.active_form = self.quota_share_form

        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()



        # Validate the active form
        # if hasattr(self, 'active_form'):
        #     valid = valid and self.active_form.is_valid()

        return valid

    def save(self, commit=True):
        return
        #instance = super().save(commit=False)

        # Save the active form
        # if hasattr(self, 'active_form'):
        #     related_instance = self.active_form.save(commit=False)
        #     related_instance.contract = instance
        #     related_instance.save()

        # if commit:
        #     instance.save()

        # return instance


class ExcessOfLossRiskForm(forms.ModelForm):
    class Meta:
        model = ExcessOfLossRisk
        fields = '__all__'

class ExcessOfLossEventForm(forms.ModelForm):
    class Meta:
        model = ExcessOfLossEvent
        fields = '__all__'

class QuotaShareForm(forms.ModelForm):
    class Meta:
        model = QuotaShare
        fields = '__all__'