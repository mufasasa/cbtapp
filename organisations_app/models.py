from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

EXAM_STATUS = (
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ('archived', 'Archived'),
)

COMPLAIN_STATUS = (
    ('not_attended', 'Not Attended'),
    ('waiting', 'Waiting'),
    ('cleared', 'Cleared'),
)






class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class OrganisationAdmin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='admins')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    


class Examination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    total_marks = models.IntegerField(blank=True, null=True)
    passing_marks = models.IntegerField(blank=True, null=True)
    questions = models.JSONField(default=list, blank=True, null=True)
    candidates = models.ManyToManyField('candidates_app.Candidate', related_name='examinations', blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='examinations')
    status = models.CharField(max_length=100, choices=EXAM_STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    

class OrganisationComplain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='complains')
    topic = models.CharField(max_length=100)
    message = models.TextField()
    status =  models.CharField(max_length=100, choices=COMPLAIN_STATUS, default='not_attended')
    created_at = models.DateTimeField(auto_now_add=True)
    admin  = models.ForeignKey(OrganisationAdmin, on_delete=models.CASCADE, related_name='complains')
    def __str__(self):
        return self.message
    

class CandidateExam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey('candidates_app.Candidate', on_delete=models.CASCADE, related_name='candidate_exams')
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='candidate_exams')
    exam_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    candidate_answers = models.JSONField(default=list, blank=True, null=True)