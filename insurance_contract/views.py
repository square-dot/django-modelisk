from django.shortcuts import render, redirect
from .forms import ContractForm

def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            return redirect('contracts')
    else:
        form = ContractForm()

    return render(request, 'create_contract.html', {'form': form})
