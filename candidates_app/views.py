from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from candidates_app.utils import auto_grade_exam
from .models import *
from django.contrib.auth import get_user_model
from organisations_app.serializers import *
from authentication.authentication import *





class FetchCandidateExamView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]


    def  get(self, request, exam_number):

        candidate_exam = CandidateExam.objects.get(exam_number=exam_number)
        if candidate_exam.candidate.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam = candidate_exam.examination
        
        serializer = ExaminationDetailSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class SubmitCandidateExam(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    def put(self, request, exam_number):
        candidate_exam = CandidateExam.objects.get(exam_number=exam_number)
        if candidate_exam.candidate.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam = candidate_exam.examination
        
        submitted_answers = request.data.get('questions', [])
        
        for answer_data in submitted_answers:
            question_id = answer_data.get('id')
            answer = answer_data.get('response')
            
            question = Question.objects.get(id=question_id, examination=exam)
            
            CandidateAnswer.objects.create(
                candidate=candidate_exam.candidate,
                question=question,
                answer=answer
            )
        
        candidate_exam.status = 'submitted'
        candidate_exam.save()

        # Auto grade the exam if auto_grade is set to true
        if exam.auto_grade:
            candidate_exam.auto_grade_exam()

        return Response(status=status.HTTP_200_OK)