from django.urls import path
from . import views

urlpatterns = [
    path("experience-analysis", views.experience_analysis, name="experience-analysis"),
]