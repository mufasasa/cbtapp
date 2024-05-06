from django.urls import path, re_path
from .views import *


urlpatterns = [

    path('organisation_admins/', OrganisationAdminListCreateView.as_view(), name='organisation_admins'),
    path('organisation_admins/<uuid:pk>/', OrganisationAdminDetailView.as_view(), name='organisation_admin_detail'),
    path('super_admins/', SuperAdminListCreateView.as_view(), name='super_admins'),
    path('super_admins/<uuid:pk>/', SuperAdminDetailView.as_view(), name='super_admin_detail'),
    path('reception_staff/', ReceptionStaffListCreateView.as_view(), name='reception_staff'),
    path('reception_staff/<uuid:pk>/', ReceptionStaffDetailView.as_view(), name='reception_staff_detail'),
    path('organisation/<uuid:organisation_id>/activate/', SuperAdminActivateOrganisationView.as_view(), name='activate_organisation'),
    path('organisation/<uuid:organisation_id>/deactivate/', SuperAdminDeactivateOrganisationView.as_view(), name='deactivate_organisation'),

    # complaints
    path('complains/', SuperAdminGetAllComplainsView.as_view(), name='complains'),
    path('complains/<uuid:complain_id>/', SuperAdminGetComplainView.as_view(), name='complain_detail'),
    path('complains/<uuid:complain_id>/reply/', AdminReplyOrganisationComplainView.as_view(), name='reply_complain'),


    path('all_organisations/', SuperAdminListAllOrganisationsView.as_view(), name='all_organisations'),
    path('all_exams/', AdminGetAllExamsView.as_view(), name='admin_all_exams'),
    path('all_exam_candidates/', AdminGetAllExamCandidates.as_view(), name='all_exam_candidates'),


    # admid exam candidate
    path('admit_exam_candidate/<uuid:candidate_exam_id>/', AdminMarkCandidateAdmittedView.as_view(), name='admit_exam_candidate'),


    # visitors
    path('visitors/', VisitorListCreateView.as_view(), name='visitors'),
    path('visitors/<uuid:visitor_id>/', VisitorDetailView.as_view(), name='visitor_detail'),
    
]