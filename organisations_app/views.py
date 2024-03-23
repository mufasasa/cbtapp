from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.models import TimedAuthToken
from authentication.utils  import user_is_in_entity, get_user_entity_instance, user_is_staff_of_organization










class OrganisationListCreateView(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthToken]

    # list all organisations
    def get(self, request):
        organisations = Organisation.objects.all()
        serializer = OrganisationCreateSerializer(organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new organisation
    def post(self, request):
        serializer = OrganisationCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # create a new user
            user = get_user_model().objects.create_user(
                username=request.data['email'],
                password=request.data['password'],
                email=request.data['email']
            )

            # create a new organisation admin
            OrganisationAdmin.objects.create(
                user=user,
                organisation=Organisation.objects.get(pk=serializer.data['id'])
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthToken]

    # list all candidates
    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new candidate
    def post(self, request):
        serializer = CandidateSerializer(data=request.data)

        # create a new user
        user = get_user_model().objects.create_user(
            username=request.data['email'],
            password=request.data['password'],
            email=request.data['email']
        )

        # create a new candidate
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthToken]

    # retrieve a candidate
    def get(self, request, pk):
        candidate = Candidate.objects.get(pk=pk)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a candidate
    def put(self, request, pk):
        candidate = Candidate.objects.get(pk=pk)
        serializer = CandidateSerializer(candidate, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # delete a candidate
    def delete(self, request, pk):
        candidate = Candidate.objects.get(pk=pk)
        candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrganisationListCreateExamsView(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthToken]

    # list all exams of an organisation
    def get(self, request, organisation_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        organisation = Organisation.objects.get(pk=pk)
        exams = organisation.examinations.all()
        serializer = ExaminationSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new exam for an organisation
    def post(self, request, organisation_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateExamSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class OrganisationExaminationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Examination.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthToken]

    # retrieve an examination
    def get(self, request, organisation_id, exam_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam = Examination.objects.get(pk=exam_id)
        serializer = ExaminationSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update an examination
    def put(self, request, organisation_id, exam_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam = Examination.objects.get(pk=exam_id)
        serializer = CreateExamSerializer(exam, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # delete an examination
    def delete(self, request, organisation_id, exam_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam = Examination.objects.get(pk=exam_id)
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)