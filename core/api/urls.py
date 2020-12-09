from django.urls import path

from . import views

urlpatterns = [
    path("beats/", views.BeatsView.as_view()),
    path("beats/by_period/", views.ListPeriodBeatsView.as_view()),
    path("/company/faults/", views.ListCompanyFaults.as_view()),
    path("/employees/<int:emp_id>/faults/", views.ListEmployeeFaults.as_view()),
]