from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .forms import ContractForm
from .models import Contract, Company, Program


def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            return redirect('contracts')
    else:
        form = ContractForm()

    return render(request, 'insurance_contract/create_contract.html', {'form': form})

class ContractDetailView(DetailView):
    model = Contract
    template_name = 'insurance_contract/contract_detail.html'

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'insurance_contract/program_detail.html'

class CompanyDetailView(DetailView):
    model = Company

class ContractsListView(ListView):
    model = Contract
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
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

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Company"
        context["object_plural_name"] = "Companies"
        return context

class ProgramsListView(ListView):
    model = Program
    paginate_by = 20
    context_object_name = "object_list"
    template_name = "base_list.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Program"
        context["object_plural_name"] = "Programs"
        return context