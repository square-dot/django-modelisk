from django.urls import path

from . import views

#list of models
urlpatterns = [
    path("contracts/", views.LayersListView.as_view(), name="contracts"),
    path("companies/", views.CompaniesListView.as_view(), name="companies"),
    path("programs/", views.ProgramsListView.as_view(), name="programs"),
    path("risk-profiles/", views.RiskProfilesListView.as_view(), name="risk-profiles"),
    path("loss-profiles/", views.LossProfilesListView.as_view(), name="loss-profiles"),
    path("reference-data", views.reference_data, name="reference-data"),
    path("business-data", views.business_data, name="business-data"),
    path("analysis", views.analysis, name="analysis-list"),
]

#details views
urlpatterns.extend((
    path("program/<str:code>/", views.ProgramDetailView.as_view(), name="program-detail"),
    path("layer/<str:code>", views.LayerDetailView.as_view(), name="layer"),
    path("company/<int:pk>", views.CompanyDetailView.as_view(), name="company-detail"),
    path("program/<str:code>/", views.ProgramDetailView.as_view(), name="program-detail"),
    path("risk-profile/<str:code>/", views.RiskProfileDetailView.as_view(), name="risk-profile-detail"),
    path("loss-profile/<str:code>/", views.LossProfileDetailView.as_view(), name="loss-profile-detail"),
    path("exposure-analysis/<str:code>", views.ExposureAnalysisDetailView.as_view(), name="exposure-analysis-detail"),
))

#creation views
urlpatterns.extend((
    path("contract-creation/", views.contract_creation, name="contract-creation"),
    path("experience-analysis-creation", views.experience_analysis_creation, name="experience-analysis-creation"),
    path("exposure-analysis-creation", views.exposure_analysis_creation, name="exposure-analysis-creation"),

))