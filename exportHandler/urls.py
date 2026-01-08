from django.urls import path
from . import views

urlpatterns = [
    path('excel/', views.export_schedule_excel, name='export_excel'),
]