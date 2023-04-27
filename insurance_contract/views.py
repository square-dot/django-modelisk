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

class CompaniesListView(ListView):
    model = Company
    paginate_by = 20
    ordering = ["name", ]

class ProgramsListView(ListView):
    model = Program
    paginate_by = 20