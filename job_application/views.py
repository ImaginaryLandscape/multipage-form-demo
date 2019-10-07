import datetime, pytz
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from . import constants
from .forms import BaseApplicationForm
from .models import JobApplication

def get_job_application_from_hash(session_hash):
    # Find and return an unexpired, not-yet-completed JobApplication
    # with a matching session_hash, or None if no such object exists.
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    max_age = 300  # Or make this a setting in "settings.py"
    exclude_before = now - datetime.timedelta(seconds=max_age)
    return JobApplication.objects.filter(
        session_hash=session_hash,
        modified__gte=exclude_before
    ).exclude(
        stage=constants.COMPLETE
    ).first()


class JobApplicationView(FormView):
    template_name = 'job_application/job_application.html'
    job_application = None
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        session_hash = request.session.get("session_hash", None)
        # Get the job application for this session. It could be None.
        self.job_application = get_job_application_from_hash(session_hash)
        # Attach the request to "self" so "form_valid()" can access it below.
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # This data is valid, so set this form's session hash in the session.
        self.request.session["session_hash"] = form.instance.session_hash
        current_stage = form.cleaned_data.get("stage")
        # Get the next stage after this one.
        new_stage = constants.STAGE_ORDER[constants.STAGE_ORDER.index(current_stage)+1]
        form.instance.stage = new_stage
        form.save()  # This will save the underlying instance.
        if new_stage == constants.COMPLETE:
            return redirect(reverse("job_application:thank_you"))
        # else
        return redirect(reverse("job_application:job_application"))

    def get_form_class(self):
        # If we found a job application that matches the session hash, look at
        # its "stage" attribute to decide which stage of the application we're
        # on. Otherwise assume we're on stage 1.
        stage = self.job_application.stage if self.job_application else constants.STAGE_1
        # Get the form fields appropriate to that stage.
        fields = JobApplication.get_fields_by_stage(stage)
        # Use those fields to dynamically create a form with "modelform_factory"
        return modelform_factory(JobApplication, BaseApplicationForm, fields)
    
    def get_form_kwargs(self):
        # Make sure Django uses the same JobApplication instance we've already been
        # working on. Otherwise it will instantiate a new one after every submit.
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.job_application
        return kwargs


class JobApplicationThankYouView(TemplateView):
    template_name = 'job_application/thank_you.html'
