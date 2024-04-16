from django.urls import path, re_path
from .views import *


urlpatterns = [

    path('organisations/', OrganisationListCreateView.as_view(), name='organisations'),
    path('organisation_detail/<uuid:organisation_id>/', OrganisationDetailView.as_view(), name='organisation_detail'),
    path('candidates/', CandidateListCreateView.as_view(), name='candidates'),
    path('candidates/<uuid:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
    path('organisation/exams/', OrganisationListCreateExamsView.as_view(), name='organisation_exams'),
    path('organisation/exam/<uuid:exam_id>/', OrganisationExaminationDetailView.as_view(), name='organisation_exam_detail'),
    path('organisation/exam/<uuid:exam_id>/candidates/', OrganisationGetExamCandidatesView.as_view(), name='organisation_exam_candidates'),
    path('organisation/exam/<uuid:exam_id>/archive_exam/', OrganisationArchiveExaminationView.as_view(), name='organisation_exam_archive'),
    path('organisation/candidates/',OrganisationListCreateCandidatesView.as_view(), name='organisation_candidates'),
    path('organisation/candidates/<uuid:candidate_id>/', OrganisationCandidateDetailView.as_view(), name='organisation_candidate_detail'),

    path('organisation/complains/', OrganisationComplainListCreateView.as_view(), name='organisation_complains'),
    path('organisation/complains/<uuid:complain_id>/', OrganisationComplainDetailView.as_view(), name='organisation_complain_detail'),
    path('exam/<uuid:exam_id>/candidates/', RetreiveExamCandidatesView.as_view(), name='exam_candidates'),

]