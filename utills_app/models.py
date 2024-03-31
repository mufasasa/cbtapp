import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FileUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/')
    organisation = models.ForeignKey('organisations_app.Organisation', on_delete=models.CASCADE, related_name='uploads', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads', blank=True, null=True)
    file_size = models.CharField(max_length=100, blank=True, null=True)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.namex


