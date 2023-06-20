from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from analysis.forms import ContractForm, CreateConvolution
from analysis.functions.Convolution import convolve_all
from analysis.functions.Plot import plot_empirical_distribution
from analysis.models.contract.BaseContract import BaseContract
from analysis.models.contract.ExcessOfLossEvent import ExcessOfLossEvent
from analysis.models.contract.ExcessOfLossRisk import ExcessOfLossRisk
from analysis.models.contract.Program import Program
from analysis.models.contract.QuotaShare import QuotaShare
from analysis.models.ExposureAnalysis import ExposureAnalysis
from analysis.models.LossProfile import LossProfile
from analysis.models.ProbabilityDistribution import (
    EmpiricalDistribution,
    ProbabilityDistribution,
)
from analysis.models.reference_value.Code import Code
from analysis.models.reference_value.Company import Company
from analysis.models.RiskProfile import RiskProfile


def contract_creation(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            return redirect("contracts")
    else:
        form = ContractForm()

    return render(request, "analysis/contract_creation.html", {"form": form})


class QuotaShareDetailView(DetailView):
    model = QuotaShare
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(
            numeric_code=int(code[1:])
        )
        return self.model.objects.get(code=my_code)


class ExcessOfLossRiskDetailView(DetailView):
    model = ExcessOfLossRisk
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(
            numeric_code=int(code[1:])
        )
        return self.model.objects.get(code=my_code)


class ExcessOfLossEventDetailView(DetailView):
    model = ExcessOfLossEvent
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(
            numeric_code=int(code[1:])
        )
        return self.model.objects.get(code=my_code)


class ProgramDetailView(DetailView):
    model = Program
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        my_code = Code.objects.filter(alphabetic_code=code[0]).get(
            numeric_code=int(code[1:])
        )
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


class LossProfilesListView(ListView):
    model = LossProfile
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
        code = self.kwargs.get("code")
        my_code = Code.get_code(code)
        return self.model.objects.get(code=my_code)


class LossProfileDetailView(DetailView):
    model = LossProfile
    context_object_name = "object"
    template_name = "base_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        my_code = Code.get_code(code)
        return self.model.objects.get(code=my_code)


def experience_analysis_creation(request):
    return render(request, "analysis/experience_analysis_creation.html")


class ExposureAnalysisDetailView(DetailView):
    model = ExposureAnalysis
    context_object_name = "exposureanalysis"
    template_name = "analysis/exposure_analysis_detail.html"
    convolution_form = CreateConvolution

    def post(self, request, code, *args, **kwargs):
        form = self.convolution_form(request.POST)
        my_code = Code.get_code(code)
        model_obj = ExposureAnalysis.objects.get(code=my_code)
        if form.is_valid():
            my_code = Code.get_code(code)
            if form.cleaned_data["function"] == "create_convolution" and not any(
                EmpiricalDistribution.objects.filter(analysis=model_obj).filter(
                    is_total_distribution=True
                )
            ):
                lds = ProbabilityDistribution.objects.filter(analysis=model_obj)
                sample = convolve_all(list(lds))
                EmpiricalDistribution.objects.create(
                    analysis=model_obj,
                    sample=sample,
                    is_total_distribution=True,
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
            "image_path": f"media/plot_{ model_obj.code}.png",
        }
        return render(
            request, "analysis/exposure_analysis_detail.html", context=context
        )

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["form"] = CreateConvolution(initial={"function": "create_convolution"})
        context["image_path"] = f"media/plot_{self.object.code}.png"  # type: ignore
        return context

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        my_code = Code.get_code(code)
        return self.model.objects.get(code=my_code)


def reference_data(request):
    return render(request, "analysis/reference_data.html")


def business_data(request):
    return render(request, "analysis/business_data.html")


def analysis(request):
    all_analysis = ExposureAnalysis.objects.all().order_by("-last_modified")
    recent = all_analysis[0:5]

    return render(
        request,
        "analysis/analysis_list.html",
        {"analysis_list": all_analysis, "recent": recent},
    )
