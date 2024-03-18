from django.urls import path, re_path
from .views import *


urlpatters = [

    path('candidates/', CandidateListCreateView.as_view(), name='candidates'),
    path('candidates/<uuid:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
]