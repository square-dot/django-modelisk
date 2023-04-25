from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import ContractForm
from .models import Contract, Company


def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            return redirect('contracts')
    else:
        form = ContractForm()

    return render(request, 'create_contract.html', {'form': form})

class ContractsListView(ListView):
    model = Contract
    paginate_by = 20
    ordering = ["administrative_information", ]

class CompaniesListView(ListView):
    model = Company
    paginate_by = 20
    ordering = ["name", ]