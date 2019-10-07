from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('job_application:job_application'))),
    path('admin/', admin.site.urls),
    path('job_application/', include('job_application.urls', namespace='job_application'))
]
