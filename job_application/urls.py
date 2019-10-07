from django.urls import path
from .views import JobApplicationView, JobApplicationThankYouView

app_name = "job_application"

urlpatterns = [
    path('', JobApplicationView.as_view(), name="job_application"),
    path('thank-you/', JobApplicationThankYouView.as_view(), name="thank_you"),
]
