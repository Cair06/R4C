from django.urls import path
from .views import add_robot

urlpatterns = [
    path('add/', add_robot, name='add_robot'),
]
