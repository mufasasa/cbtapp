from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('upload_file', UploadFileView.as_view(), name='upload_file'),

    
]