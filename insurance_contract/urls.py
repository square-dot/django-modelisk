from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_contract, name="create_contract"),
    path("contracts/", views.ContractsListView.as_view(), name="contracts"),
]