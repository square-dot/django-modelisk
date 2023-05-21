from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from analysis.models.contract.BaseContract import BaseContract
from analysis.models.contract.ExcessOfLossRisk import ExcessOfLossRisk
from analysis.models.contract.ExcessOfLossEvent import ExcessOfLossEvent
from analysis.models.contract.QuotaShare import QuotaShare
from analysis.forms import ContractForm, CreateConvolution
from analysis.models.reference_value.Company import Company
from analysis.functions.Convolution import convolve_all
from analysis.models.ExposureAnalysis import ExposureAnalysis
from analysis.models.LossDistribution import EmpiricalDistribution, LossDistribution
from analysis.functions.Plot import plot_empirical_distribution
from analysis.models.contract.Program import Program
from analysis.models.reference_value.Code import Code
from analysis.models.RiskProfile import RiskProfile


def create_contract(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            return redirect("contracts")
    else:
        form = ContractForm()

    return render(request, "analysis/create_contract.html", {"form": form})


class QuotaShareDetailView(DetailView):
    model = QuotaShare
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get('code')
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(numeric_code=int(code[1:]))
        return self.model.objects.get(code=my_code)


class ExcessOfLossRiskDetailView(DetailView):
    model = ExcessOfLossRisk
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get('code')
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(numeric_code=int(code[1:]))
        return self.model.objects.get(code=my_code)


class ExcessOfLossEventDetailView(DetailView):
    model = ExcessOfLossEvent
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get('code')
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(numeric_code=int(code[1:]))
        return self.model.objects.get(code=my_code)


class ProgramDetailView(DetailView):
    model = Program
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get('code')
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(numeric_code=int(code[1:]))
        return self.model.objects.get(code=my_code)


class CompanyDetailView(DetailView):
    model = Company
    context_object_name = "object"
    template_name = "base_detail.html"


class ContractsListView(ListView):
    model = BaseContract
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Contract"
        context["object_plural_name"] = "Contracts"
        return context


class CompaniesListView(ListView):
    model = Company
    paginate_by = 20
    ordering = [
        "name",
    ]
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Company"
        context["object_plural_name"] = "Companies"
        return context


class ProgramsListView(ListView):
    model = Program
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Program"
        context["object_plural_name"] = "Programs"
        return context

class RiskProfilesListView(ListView):
    model = RiskProfile
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Risk profile"
        context["object_plural_name"] = "Risk profiles"
        return context

class RiskProfileDetailView(DetailView):
    model = RiskProfile
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get('code')
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(numeric_code=int(code[1:]))
        return self.model.objects.get(code=my_code)

def experience_analysis(request):
    return render(request, "analysis/experience_analysis_creation.html")


class ExposureAnalysisDetailView(DetailView):
    model = ExposureAnalysis
    context_object_name = "exposureanalysis"
    template_name = "analysis/exposure_analysis_detail.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["image_path"] = f"media/plot_{self.object.code}.png"  # type: ignore
        return context
    
    def get_object(self, queryset=None):
        code = self.kwargs.get('code')
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(numeric_code=int(code[1:]))
        return self.model.objects.get(code=my_code)


class ExposureAnalysisListView(ListView):
    model = ExposureAnalysis
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Exposure Analysis"
        context["object_plural_name"] = "Exposure Analysis"
        return context


def exposure_analysis_edit(request, pk):
    if request.method == "POST":
        model_obj = ExposureAnalysis.objects.get(pk=pk)
        form = CreateConvolution(request.POST)
        if form.is_valid():
            if form.cleaned_data["function"] == "create_convolution":
                lds = LossDistribution.objects.filter(analysis=model_obj)
                sample = convolve_all(list(lds))
                EmpiricalDistribution.objects.create(
                    analysis=model_obj, sample=sample, is_total_distribution=True
                )
                _ = plot_empirical_distribution(sample, anlysis_code=model_obj.code)
            else:
                print(form.cleaned_data["function"])
        else:
            print(form.errors.as_data())
        context = {
            "exposureanalysis": model_obj,
            "form": CreateConvolution(
                initial={"function": "create_convolution"},
            ),
        }
        return render(request, "analysis/exposure_analysis_edit.html", context=context)
    else:
        model_obj = ExposureAnalysis.objects.get(pk=pk)
        context = {
            "exposureanalysis": model_obj,
            "form": CreateConvolution(initial={"function": "create_convolution"}),
        }
        return render(request, "analysis/exposure_analysis_edit.html", context=context)
