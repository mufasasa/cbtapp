from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class Organisation(models.Model):
    idd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class OrganisationAdmin(models.Model):
    idd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='admins')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    