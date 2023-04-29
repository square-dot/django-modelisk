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