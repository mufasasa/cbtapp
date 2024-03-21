from django.db import models
from django.contrib.auth import get_user_model
from organisations_app.models import Organisation
import uuid

User = get_user_model()



class Candidate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    organisation = models.ManyToManyField(Organisation, related_name='candidates')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
