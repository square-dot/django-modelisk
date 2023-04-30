from django.urls import path
from . import views

urlpatterns = [
    path("experience-analysis", views.experience_analysis, name="experience-analysis-creation"),
    path("exposure-analysis-detail/<int:pk>", views.ExposureAnalysisDetailView.as_view(), name="exposure-analysis-detail"),
    path("exposure-analysis", views.ExposureAnalysisListView.as_view(), name="exposure-analysis"),
]