from django.shortcuts import render, redirect
from .forms import ContractForm
from .models import Contract
from django.views.generic import ListView

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
