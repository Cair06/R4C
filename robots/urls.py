from django.urls import path
from .views import download_weekly_report

urlpatterns = [
    path('download-weekly-report/', download_weekly_report, name='download_weekly_report'),
]