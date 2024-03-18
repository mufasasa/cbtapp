from django.urls import path, re_path
from authentication.views import *


app_name = 'authentication'


url_patterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('organisation_admins/', OrganisationAdminListCreateView.as_view(), name='organisation_admins'),
    path('organisation_admins/<uuid:pk>/', OrganisationAdminDetailView.as_view(), name='organisation_admin_detail'),
    path('super_admins/', SuperAdminListCreateView.as_view(), name='super_admins'),
    path('super_admins/<uuid:pk>/', SuperAdminDetailView.as_view(), name='super_admin_detail'),
    path('reception_staff/', ReceptionStaffListCreateView.as_view(), name='reception_staff'),
    path('reception_staff/<uuid:pk>/', ReceptionStaffDetailView.as_view(), name='reception_staff_detail'),
    path('candidates/', CandidateListCreateView.as_view(), name='candidates'),
    path('candidates/<uuid:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
]