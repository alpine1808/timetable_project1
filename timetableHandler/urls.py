from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_view, name='timetable_view'),
    path('add/<int:class_id>/', views.add_class, name='add_class'),
    path('remove/<int:item_id>/', views.remove_class, name='remove_class'),
]