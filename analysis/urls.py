from django.urls import path
from . import views

urlpatterns = [
    path("create-contract/", views.create_contract, name="create-contract"),
    path("contracts/", views.ContractsListView.as_view(), name="contracts"),
    path("companies/", views.CompaniesListView.as_view(), name="companies"),
    path("programs/", views.ProgramsListView.as_view(), name="programs"),
    path("contract/<int:pk>", views.ContractDetailView.as_view(), name="contract-detail"),
    path("company/<int:pk>", views.CompanyDetailView.as_view(), name="company-detail"),
    path("program/<int:pk>", views.ProgramDetailView.as_view(), name="program-detail"),
    path("experience-analysis", views.experience_analysis, name="experience-analysis-creation"),
    path("exposure-analysis-detail/<int:pk>", views.ExposureAnalysisDetailView.as_view(), name="exposure-analysis-detail"),
    path("exposure-analysis", views.ExposureAnalysisListView.as_view(), name="exposure-analysis"),
]