from django.urls import path, re_path
from .views import *


app_name = 'candidates_app'

urlpatterns = [
    path('fetch_exam/<str:exam_number>/', FetchCandidateExamView.as_view(), name='fetch_exam'),
    path('submit_exam/<str:exam_number>/', SubmitCandidateExam.as_view(), name='submit_exam'),
    
]