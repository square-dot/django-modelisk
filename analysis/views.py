from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from analysis.models import ExposureAnalysis

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
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["object_name"] = "Exposure Analysis"
        context["object_plural_name"] = "Exposure Analysis"
        return context