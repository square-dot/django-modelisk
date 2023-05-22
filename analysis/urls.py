from django.urls import path
from . import views

urlpatterns = [
    path("contract-creation/", views.create_contract, name="contract-creation"),
    path("contracts/", views.ContractsListView.as_view(), name="contracts"),
    path("companies/", views.CompaniesListView.as_view(), name="companies"),
    path("programs/", views.ProgramsListView.as_view(), name="programs"),
    path("risk-profiles/", views.RiskProfilesListView.as_view(), name="risk-profiles"),
    path("loss-profiles/", views.LossProfilesListView.as_view(), name="loss-profiles"),
    path("quotashare/<str:code>", views.QuotaShareDetailView.as_view(), name="quota-share"),
    path("excessoflossrisk/<str:code>", views.ExcessOfLossRiskDetailView.as_view(), name="xl-risk"),
    path("excessoflossevent/<str:code>", views.ExcessOfLossEventDetailView.as_view(), name="xl-event"),
    path("company/<int:pk>", views.CompanyDetailView.as_view(), name="company-detail"),
    path("program/<str:code>/", views.ProgramDetailView.as_view(), name="program-detail"),
    path("risk-profile/<str:code>/", views.RiskProfileDetailView.as_view(), name="risk-profile-detail"),
    path("loss-profile/<str:code>/", views.LossProfileDetailView.as_view(), name="loss-profile-detail"),
    path("experience-analysis", views.experience_analysis, name="experience-analysis-creation"),
    path("exposure-analysis-detail/<str:code>", views.ExposureAnalysisDetailView.as_view(), name="exposure-analysis-detail"),
    path("exposure-analysis", views.ExposureAnalysisListView.as_view(), name="exposure-analysis"),
    path("exposure-analysis-edit/<str:code>", views.exposure_analysis_edit, name="exposure-analysis-edit"),
]