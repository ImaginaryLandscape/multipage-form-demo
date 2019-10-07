import hashlib, random, sys
from django.db import models
from . import constants

def create_session_hash():
    hash = hashlib.sha1()
    hash.update(str(random.randint(0,sys.maxsize)).encode('utf-8'))
    return hash.hexdigest()


class JobApplication(models.Model):
    # operational
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    session_hash = models.CharField(max_length=40, unique=True)
    stage = models.CharField(max_length=10, default=constants.STAGE_1)
    # stage 1 fields
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    # stage 2 fields
    prior_experience = models.TextField(blank=True)
    # stage 3 fields
    all_is_accurate = models.BooleanField(default=False)

    hidden_fields = ['stage']
    required_fields = ['first_name', 'last_name', 'all_is_accurate']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.session_hash:
            while True:
                session_hash = create_session_hash()
                if JobApplication.objects.filter(session_hash=session_hash).count() == 0:
                    self.session_hash = session_hash
                    break

    @staticmethod
    def get_fields_by_stage(stage):
        fields = ['stage']  # Must always be present
        if stage == constants.STAGE_1:
            fields.extend(['first_name', 'last_name'])
        elif stage == constants.STAGE_2:
            fields.extend(['prior_experience'])
        elif stage == constants.STAGE_3:
            fields.extend(['all_is_accurate'])
        return fields
