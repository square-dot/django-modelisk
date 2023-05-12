from django.urls import path
from . import views

urlpatterns = [
    path("create-contract/", views.create_contract, name="create-contract"),
    path("contracts/", views.ContractsListView.as_view(), name="contracts"),
    path("companies/", views.CompaniesListView.as_view(), name="companies"),
    path("programs/", views.ProgramsListView.as_view(), name="programs"),
    path("quotashare/<int:pk>", views.QuotaShareDetailView.as_view(), name="quota-share"),
    path("excessoflossrisk/<int:pk>", views.ExcessOfLossRiskDetailView.as_view(), name="xl-risk"),
    path("excessoflossevent/<int:pk>", views.ExcessOfLossEventDetailView.as_view(), name="xl-event"),
    path("company/<int:pk>", views.CompanyDetailView.as_view(), name="company-detail"),
    path("program/<int:pk>", views.ProgramDetailView.as_view(), name="program-detail"),
    path("experience-analysis", views.experience_analysis, name="experience-analysis-creation"),
    path("exposure-analysis-detail/<int:pk>", views.ExposureAnalysisDetailView.as_view(), name="exposure-analysis-detail"),
    path("exposure-analysis", views.ExposureAnalysisListView.as_view(), name="exposure-analysis"),
    path("exposure-analysis-edit/<int:pk>", views.exposure_analysis_edit, name="exposure-analysis-edit"),
]