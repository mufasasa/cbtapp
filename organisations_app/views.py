from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.authentication import TimedAuthTokenAuthentication
from authentication.utils  import user_is_in_entity, get_user_entity_instance, user_is_staff_of_organization
from rest_framework.pagination import PageNumberPagination
from utills_app.serializers import FileUploadSerializer
from utills_app.models import FileUpload








class OrganisationListCreateView(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    
    # list all organisations
    def get(self, request):
        organisations = Organisation.objects.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new organisation
    def post(self, request):
        serializer = OrganisationCreateSerializer(data=request.data)

        if serializer.is_valid():

            user = get_user_model().objects.filter(username=request.data['email'])
            if user.exists():
                return Response({'error': 'User with email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # create a new organisation
            organisation_instance = Organisation.objects.create(
                name=request.data['name'],
                address=request.data['address'],
                phone=request.data['phone'],
                email=request.data['email'],
                website=request.data['website'] if 'website' in request.data else None,
                logo = request.data['logo'] if 'logo' in request.data else None
            )

            # create a new user
            user = get_user_model().objects.create_user(
                username=request.data['email'],
                password=request.data['password'],
                email=request.data['email']
            )

            # create a new organisation admin
            organisation_admin = OrganisationAdmin.objects.create(
                user=user,
                organisation=organisation_instance
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
         
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

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
    authentication_classes = [TimedAuthTokenAuthentication]

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
    authentication_classes = [TimedAuthTokenAuthentication]

    paginator = PageNumberPagination()

    # list all exams of an organisation
    def get(self, request, organisation_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        organisation = Organisation.objects.get(pk=organisation_id)
        exams = organisation.examinations.all()

        # sort exams by created_at, in descending order
        exams = exams.order_by('-created_at')

        page = self.paginator.paginate_queryset(exams, request)
        if page is not None:
            serializer = ExaminationSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        
        serializer = ExaminationSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new exam for an organisation
    def create(self, request, organisation_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateExamSerializer(data=request.data)

        if serializer.is_valid():
            exam = serializer.save()
            exam_id = exam.id
            return Response({"message":"successfull", "id":exam_id}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class OrganisationExaminationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Examination.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

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

        # update an examination
        exam.name = request.data['name'] if 'name' in request.data else exam.name
        exam.description = request.data['description'] if 'description' in request.data else exam.description
        exam.start_time = request.data['start_time'] if 'start_time' in request.data else exam.start_time
        exam.end_time = request.data['end_time'] if 'end_time' in request.data else exam.end_time
        exam.duration = request.data['duration'] if 'duration' in request.data else exam.duration
        exam.instructions = request.data['instructions'] if 'instructions' in request.data else exam.instructions
        exam.total_marks = request.data['total_marks'] if 'total_marks' in request.data else exam.total_marks
        exam.passing_marks = request.data['passing_marks'] if 'passing_marks' in request.data else exam.passing_marks
        exam.questions = request.data['questions'] if 'questions' in request.data else exam.questions
        exam.save()

        
        return Response({"message":"exam update successfull", "id":str(exam.id)},status=status.HTTP_200_OK)
    

    # delete an examination
    def delete(self, request, organisation_id, exam_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam = Examination.objects.get(pk=exam_id)
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class OrganusationArchiveExaminationView(generics.UpdateAPIView):
    queryset = Examination.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # archive an examination
    def put(self, request, organisation_id, exam_id):
        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam = Examination.objects.get(pk=exam_id)
        exam.status = 'archived'
        exam.save()
        return Response(status=status.HTTP_200_OK)
    


class OrganisationUploadFile(generics.CreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # upload a file
    def post(self, request, organisation_id):

        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            file_instance = FileUpload.objects.create(
                file = request.data['file'],
                user = request.user,
                organisation = organisation_instance
            )
            return Response({"file_id":str(file_instance.id)}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class OrganisationListCreateCandidatesView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # create a new candidate
    def post(self, request, organisation_id):
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = CandidateSerializer(data=request.data)


        # check if user with email already exists
        user = get_user_model().objects.filter(username=request.data['email'])
        if user.exists():
            return Response({'error': 'User with email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # create a new user
        user = get_user_model().objects.create_user(
            username=request.data['email'],
            password=request.data['password'],
            email=request.data['email']
        )

        # create a new candidate
        canditate_instance = Candidate.objects.create(
            user=user,
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            nin=request.data['nin'],
            email=request.data['email'],
            phone=request.data['phone'],
            phone2=request.data['phone2'] if 'phone2' in request.data else None,
            photo=request.data['photo'] if 'photo' in request.data else None,
            organisation=organisation_instance
        )

        
        return Response({
            "message":"candidate created successfull",
            "id":str(canditate_instance.id)
        }, status=status.HTTP_201_CREATED)
    


    def get(self, request, organisation_id):
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        candidates = organisation_instance.candidates.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class OrganisationCandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve a candidate
    def get(self, request, organisation_id, candidate_id):
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        candidate = Candidate.objects.get(pk=candidate_id)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a candidate
    def put(self, request, organisation_id, candidate_id):
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        candidate = Candidate.objects.get(pk=candidate_id)

        candidate.first_name = request.data['first_name'] if 'first_name' in request.data else candidate.first_name
        candidate.last_name = request.data['last_name'] if 'last_name' in request.data else candidate.last_name
        candidate.nin = request.data['nin'] if 'nin' in request.data else candidate.nin
        candidate.email = request.data['email'] if 'email' in request.data else candidate.email
        candidate.phone = request.data['phone'] if 'phone' in request.data else candidate.phone
        candidate.phone2 = request.data['phone2'] if 'phone2' in request.data else candidate.phone2
        candidate.photo = request.data['photo'] if 'photo' in request.data else candidate.photo
        candidate.save()

       
        
        return Response({"message":"candidate update successfull", "id":str(candidate.id)},status=status.HTTP_200_OK)
    

    # delete a candidate
    def delete(self, request, organisation_id, candidate_id):
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        candidate = Candidate.objects.get(pk=candidate_id)
        candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
