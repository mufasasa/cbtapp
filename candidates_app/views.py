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
        # modify the cndidate exam questions to remove the answer property
        exam.questions = [{**question, 'answer': None} for question in exam.questions] 
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
        
        data = request.data
        candidate_exam.candidate_answers = data
        candidate_exam.save()

        # auto grade the exam if auto grade is  set  to true
        if exam.auto_grade:
            
            candidate_exam = auto_grade_exam(candidate_exam, exam)

            data = {'score':candidate_exam.score,
                    'status':candidate_exam.status}



        return Response(status=status.HTTP_200_OK, data=data)