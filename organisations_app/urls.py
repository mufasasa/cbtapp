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
    path('organisation/<uuid:organisation_id>/upload_candidates/', CandidateBatchUploadView.as_view(), name='upload_candidates'),

    path('organisation/complains/', OrganisationComplainListCreateView.as_view(), name='organisation_complains'),
    path('organisation/complains/<uuid:complain_id>/', OrganisationComplainDetailView.as_view(), name='organisation_complain_detail'),
    path('exam/<uuid:exam_id>/candidates/', RetreiveExamCandidatesView.as_view(), name='exam_candidates'),
    path('exam/<uuid:exam_id>/admitted_candidates_count/', RetrieveAdmittedCandidatesCount.as_view(), name='admitted_candidates_count'),

    path('candidate_exam/<uuid:candidate_exam_id>/', CandidateExamDetailView.as_view(), name='candidate_exam_detail'),
    path('candidate_exam/<uuid:candidate_id>/<uuid:exam_id>/analysis/', CandidateAnalysisReportView.as_view(), name='candidate_exam_analysis_report'),

    path('organisation/<uuid:organisation_id>/deactivate/', DeactivateOrganisationAccount.as_view(), name='deactivate_organisation'),

    path('exam/<uuid:exam_id>/questions/', ExamQuestionListCreateView.as_view(), name='exam_question_list_create'),
    path('exam/<uuid:exam_id>/questions/<uuid:pk>/', ExamQuestionDetailView.as_view(), name='exam_question_detail'),

    path('exam/<uuid:exam_id>/candidate/<uuid:candidate_id>/extend_time/', ExtendCandidateExamTimeView.as_view(), name='extend_candidate_exam_time'),

    path('question/<uuid:question_id>/analysis/', QuestionAnalysisReportView.as_view(), name='question_analysis_report'),
    path('exam/<uuid:exam_id>/analysis/', ExamAnalysisReportView.as_view(), name='exam_analysis_report'),
    

]