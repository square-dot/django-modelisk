from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from analysis.forms import ContractForm, CreateConvolution
from analysis.models.Company import Company
from analysis.models.Contract import Contract
from analysis.models.Convolution import convolve
from analysis.models.ExposureAnalysis import ExposureAnalysis
from analysis.models.LossDistribution import LossDistribution, EmpiricalDistribution
from analysis.models.Program import Program


def create_contract(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            return redirect("contracts")
    else:
        form = ContractForm()

    return render(request, "analysis/create_contract.html", {"form": form})


class ContractDetailView(DetailView):
    model = Contract
    context_object_name = "object"
    template_name = "base_detail.html"


class ProgramDetailView(DetailView):
    model = Program
    context_object_name = "object"
    template_name = "base_detail.html"


class CompanyDetailView(DetailView):
    model = Company
    context_object_name = "object"
    template_name = "base_detail.html"


class ContractsListView(ListView):
    model = Contract
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


def experience_analysis(request):
    return render(request, "analysis/experience_analysis_creation.html")


class ExposureAnalysisDetailView(DetailView):
    model = ExposureAnalysis
    context_object_name = "exposureanalysis"
    template_name = "analysis/exposure_analysis_detail.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:  # type: ignore
        context = super().get_context_data(**kwargs)
        context["image_path"] = "media/trex.jpg"
        return context

    def post(self, request, pk):
        model_obj = ExposureAnalysis.objects.get(pk=pk)
        form = CreateConvolution(request.POST)
        if form.is_valid():
            lds = LossDistribution.objects.filter(analysis=model_obj)
            sample = convolve(
                list(lds)
            )
            EmpiricalDistribution.objects.create(analysis=model_obj, sample=sample, is_total_distribution=True)
        else:
            lds = LossDistribution.objects.filter(analysis=model_obj)
            sample = convolve(
                list(lds)
            )
            EmpiricalDistribution.objects.create(analysis=model_obj, sample=sample, is_total_distribution=True)
        model_obj = ExposureAnalysis.objects.get(pk=pk)
        context = {"exposureanalysis": model_obj,}
        return render(request, self.template_name, context=context)


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
    # model_id = request.GET.get('pk')
    model_obj = ExposureAnalysis.objects.get(pk=pk)
    context = {
        "exposureanalysis": model_obj,
        "form": CreateConvolution(initial={"pk": pk}),
    }
    return render(request, "analysis/exposure_analysis_edit.html", context=context)
