from django.urls import path, re_path
from .views import *


urlpatterns = [

    path('organisation_admins/', OrganisationAdminListCreateView.as_view(), name='organisation_admins'),
    path('organisation_admins/<uuid:pk>/', OrganisationAdminDetailView.as_view(), name='organisation_admin_detail'),
    path('super_admins/', SuperAdminListCreateView.as_view(), name='super_admins'),
    path('super_admins/<uuid:pk>/', SuperAdminDetailView.as_view(), name='super_admin_detail'),
    path('reception_staff/', ReceptionStaffListCreateView.as_view(), name='reception_staff'),
    path('reception_staff/<uuid:pk>/', ReceptionStaffDetailView.as_view(), name='reception_staff_detail'),
]