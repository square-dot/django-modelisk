from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models.Contract import Contract
from .models.Company import Company
from analysis.models.ExposureAnalysis import ExposureAnalysis

from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .forms import ContractForm
from .models.Program import Program



def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            return redirect('contracts')
    else:
        form = ContractForm()

    return render(request, 'analysis/create_contract.html', {'form': form})

class ContractDetailView(DetailView):
    model = Contract
    context_object_name = "object"
    template_name = 'base_detail.html'

class ProgramDetailView(DetailView):
    model = Program
    context_object_name = "object"
    template_name = 'base_detail.html'

class CompanyDetailView(DetailView):
    model = Company
    context_object_name = "object"
    template_name = 'base_detail.html'

class ContractsListView(ListView):
    model = Contract
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]: # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Contract"
        context["object_plural_name"] = "Contracts"
        return context

class CompaniesListView(ListView):
    model = Company
    paginate_by = 20
    ordering = ["name", ]
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]: # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Company"
        context["object_plural_name"] = "Companies"
        return context

class ProgramsListView(ListView):
    model = Program
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]: # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Program"
        context["object_plural_name"] = "Programs"
        return context

def experience_analysis(request):
    return render(request, 'analysis/experience_analysis_creation.html')

class ExposureAnalysisDetailView(DetailView):
    model = ExposureAnalysis
    template_name = 'analysis/exposure_analysis_detail.html'

class ExposureAnalysisListView(ListView):
    model = ExposureAnalysis
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]: # type: ignore
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Exposure Analysis"
        context["object_plural_name"] = "Exposure Analysis"
        return context