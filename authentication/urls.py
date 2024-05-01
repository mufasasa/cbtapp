from django.urls import path, re_path
from authentication.views import *


app_name = 'authentication'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('candidate_login/', CandidateLogin.as_view(), name='candidate_login'),
]