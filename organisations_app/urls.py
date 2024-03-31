from django.urls import path, re_path
from .views import *


urlpatterns = [

    path('organisations/', OrganisationListCreateView.as_view(), name='organisations'),
    path('candidates/', CandidateListCreateView.as_view(), name='candidates'),
    path('candidates/<uuid:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
    path('organisation/<uuid:organisation_id>/exams/', OrganisationListCreateExamsView.as_view(), name='organisation_exams'),
    path('organisation/<uuid:organisation_id>/exam/<uuid:exam_id>/', OrganisationExaminationDetailView.as_view(), name='organisation_exam_detail'),
    path('organisation/<uuid:organisation_id>/exam/<uuid:exam_id>/archive_exam/', OrganisationArchiveExaminationView.as_view(), name='organisation_exam_archive'),
    path('organisation/<uuid:organisation_id>/candidates/',OrganisationListCreateCandidatesView.as_view(), name='organisation_candidates'),
    path('organisation/<uuid:organisation_id>/candidates/<uuid:candidate_id>/', OrganisationCandidateDetailView.as_view(), name='organisation_candidate_detail'),

]