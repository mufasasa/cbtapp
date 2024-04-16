from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
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