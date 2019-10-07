from django.contrib import admin
from .models import JobApplication

class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    list_display = ('created', 'first_name', 'last_name', 'stage')
    readonly_fields = ('stage',)
    exclude = ('session_hash',)

admin.site.register(JobApplication, JobApplicationAdmin)
