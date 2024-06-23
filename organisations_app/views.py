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
from .utils import *
import pandas as pd






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

        if request.query_params.get('name'):
            # search for either first name or last name containig name
            candidates = candidates.filter(first_name__icontains=request.query_params.get('name')) | candidates.filter(last_name__icontains=request.query_params.get('name'))

        if request.query_params.get('email'):
            candidates = candidates.filter(email__icontains=request.query_params.get('email'))

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
    def get(self, request):
        organisation_id = request.query_params.get('organisation_id', None)
    
        organisation = None
        if  organisation_id:
            organisation = Organisation.objects.get(pk=organisation_id)
        
        if organisation:
            exams = organisation.examinations.all()
        else:
            exams = Examination.objects.all()


        if request.query_params.get('status'):
            exams = exams.filter(status=request.query_params.get('status'))

        # sort exams by created_at, in descending order
        exams = exams.order_by('-created_at')

        page = self.paginator.paginate_queryset(exams, request)
        if page is not None:
            serializer = ExaminationSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        
        serializer = ExaminationSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new exam for an organisation
    def create(self, request):
        organisation_id = request.data['organisation']

        if not user_is_staff_of_organization(request.user, Organisation.objects.get(pk=organisation_id)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateExamSerializer(data=request.data)

        if serializer.is_valid():
            exam = serializer.save()
            exam_id = exam.id

            #  create candidate exam instances for each candidate
            candidates_ids = request.data.get('candidates', [])
            for candidate_id in candidates_ids:
                candidate = Candidate.objects.get(pk=candidate_id)
                CandidateExam.objects.create(
                    candidate=candidate,
                    examination=exam,
                    exam_number = generate_exam_number()
                )

            return Response({"message":"successfull", "id":exam_id}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class OrganisationExaminationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Examination.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve an examination
    def get(self, request, exam_id):
        exam = Examination.objects.get(pk=exam_id)
        organisation = exam.organisation
        # if not user_is_staff_of_organization(request.user, organisation):
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ExaminationSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update an examination
    def put(self, request, exam_id):
        exam = Examination.objects.get(pk=exam_id)
        organisation = exam.organisation
        if not user_is_staff_of_organization(request.user, organisation):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
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
    def delete(self, request, exam_id):
        exam = Examination.objects.get(pk=exam_id)
        organisation = exam.organisation
        if not user_is_staff_of_organization(request.user, organisation):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class OrganisationArchiveExaminationView(generics.UpdateAPIView):
    queryset = Examination.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # archive an examination
    def put(self, request, exam_id):
        exam =  Examination.objects.get(pk=exam_id)
        organisation_instance = exam.organisation
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
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
    paginator = PageNumberPagination()

    # create a new candidate
    def post(self, request):
        organisation_id = request.data.get('organisation_id')
        if not organisation_id:
            return Response({'error': 'organisation_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        

        # check if user with email already exists
        user = get_user_model().objects.filter(username=request.data['email'])
        if user.exists():
            user = user.first()

        else:
        
            # create a new user
            user = get_user_model().objects.create_user(
                username=request.data['email'],
                password='0000',
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
        )
        canditate_instance.organisation = organisation_instance
        canditate_instance.save()
        

        
        return Response({
            "message":"candidate created successfull",
            "id":str(canditate_instance.id)
        }, status=status.HTTP_201_CREATED)
    


    def get(self, request):
        organisation_id = request.query_params.get('organisation_id')
        if  organisation_id:
            organisation_instance = Organisation.objects.get(pk=organisation_id)
            candidates = organisation_instance.candidates.all()
        else:
            candidates = Candidate.objects.all()
            
        if request.query_params.get('name'):
            # search for either first name or last name containig name
            candidates = candidates.filter(first_name__icontains=request.query_params.get('name')) | candidates.filter(last_name__icontains=request.query_params.get('name'))

        page = self.paginator.paginate_queryset(candidates, request)
        if page is not None:
            serializer = CandidateSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class OrganisationCandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve a candidate
    def get(self, request, candidate_id):
        candidate = Candidate.objects.get(pk=candidate_id)
        organisation_instance = candidate.organisation
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        candidate = Candidate.objects.get(pk=candidate_id)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a candidate
    def put(self, request, candidate_id):
        candidate = Candidate.objects.get(pk=candidate_id)
        organisation_instance = candidate.organisation
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        

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
    def delete(self, request, candidate_id):
        candidate = Candidate.objects.get(pk=candidate_id)
        organisation_instance = candidate.organisation

        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrganisationGetExamCandidatesView(generics.ListAPIView):
    # get all candidates of an exam include pagination and search
    queryset = Examination.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]
    paginator = PageNumberPagination()


    def get(self, request, exam_id):
        exam = Examination.objects.get(pk=exam_id)
        organisation_instance = exam.organisation
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        candidates = exam.candidates.all()

        if request.query_params.get('name'):
            # search for either first name or last name containig name
            candidates = candidates.filter(first_name__icontains=request.query_params.get('name')) | candidates.filter(last_name__icontains=request.query_params.get('name'))

        page = self.paginator.paginate_queryset(candidates, request)
        if page is not None:
            serializer = CandidateSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class OrganisationComplainListCreateView(generics.ListCreateAPIView):
    queryset = OrganisationComplain.objects.all()
    serializer_class = OrganisationComplainSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]
    paginator = PageNumberPagination()

    # list all complains
    def get(self, request):
        organisation_id = request.query_params.get('organisation_id')
        
        if organisation_id:
            organisation_instance = Organisation.objects.get(pk=organisation_id)
            complains = organisation_instance.complains.all()
        else:
            complains = OrganisationComplain.objects.all()

        page = self.paginator.paginate_queryset(complains, request)
        if page is not None:
            serializer = OrganisationComplainSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        
        serializer = OrganisationComplainSerializer(complains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new complain
    def post(self, request):
        organisation_id = request.data.get('organisation_id')
        if not organisation_id:
            return Response({'error': 'organisation_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        admin_instance = OrganisationAdmin.objects.filter(user=request.user, organisation=organisation_instance)
        if not admin_instance.exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        admin_instance = admin_instance.first()
        
        # serializer = OrganisationComplainSerializer(data=request.data)
        # create the complain
        complain = OrganisationComplain.objects.create(
            organisation=organisation_instance,
            topic=request.data['topic'],
            message=request.data['message'],
            admin=admin_instance
        )
        return Response({"message":"complain created successfull", "id":str(complain.id)}, status=status.HTTP_201_CREATED)
        
    

class OrganisationComplainDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganisationComplain.objects.all()
    serializer_class = OrganisationComplainSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve a complain
    def get(self, request, complain_id):
        complain = OrganisationComplain.objects.get(pk=complain_id)
        organisation_instance = complain.organisation

        # if not user_is_staff_of_organization(request.user, organisation_instance):
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = OrganisationComplainSerializer(complain)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a complain
    def put(self, request, complain_id):
        complain = OrganisationComplain.objects.get(pk=complain_id)
        organisation_instance = complain.organisation

        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        

        complain.topic = request.data['topic'] if 'topic' in request.data else complain.topic
        complain.message = request.data['message'] if 'message' in request.data else complain.message
        complain.save()

        
        return Response({"message":"complain update successfull", "id":str(complain.id)},status=status.HTTP_200_OK)
    

    # delete a complain
    def delete(self, request, complain_id):
        complain = OrganisationComplain.objects.get(pk=complain_id)
        organisation_instance = complain.organisation

        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        complain.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class OrganisationDetailView(generics.RetrieveUpdateAPIView):
    "fetch and update organisation details"
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    def get(self, request, organisation_id):
        organisation = Organisation.objects.get(pk=organisation_id)
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, organisation_id):
        organisation_instance = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation_instance):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        organisation_instance.name = request.data['name'] if 'name' in request.data else organisation_instance.name
        organisation_instance.address = request.data['address'] if 'address' in request.data else organisation_instance.address
        organisation_instance.phone = request.data['phone'] if 'phone' in request.data else organisation_instance.phone
        organisation_instance.email = request.data['email'] if 'email' in request.data else organisation_instance.email
        organisation_instance.website = request.data['website'] if 'website' in request.data else organisation_instance.website
        organisation_instance.logo = request.data['logo'] if 'logo' in request.data else organisation_instance.logo

        organisation_instance.save()
        return Response({"message":"organisation update successfull", "id":str(organisation_instance.id)},status=status.HTTP_200_OK)
    


class RetreiveExamCandidatesView(generics.RetrieveAPIView):
    
    """
    fetch the candidates of an exam by examination id
    """
    paginator = PageNumberPagination()

    def  get(self, request, exam_id):

        exam = Examination.objects.get(id=exam_id)
        
        candidates = CandidateExam.objects.filter(examination=exam)
        page = self.paginator.paginate_queryset(candidates, request)
        if page is not None:
            serializer = CandidateExamSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        
        serializer = CandidateExamSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class RetrieveAdmittedCandidatesCount(generics.RetrieveAPIView):
    """
    fetch the count of admitted candidates of an exam by examination id
    """
    def get(self, request, exam_id):
        exam = Examination.objects.get(id=exam_id)
        candidates = CandidateExam.objects.filter(examination=exam, status="admitted")
        count = candidates.count()
        total_candidates =  CandidateExam.objects.filter(examination=exam).count()
        return Response({"admitted_candidates":count, "total_candidates": total_candidates}, status=status.HTTP_200_OK)
    



class CandidateBatchUploadView(generics.CreateAPIView):
    """
    API view to upload a batch of candidates from an Excel or CSV file.
    """
    serializer_class = CandidateUploadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    def post(self, request, organisation_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organisation = Organisation.objects.get(pk=organisation_id)
        if not user_is_staff_of_organization(request.user, organisation):
            return Response(status=status.HTTP_403_FORBIDDEN)

        file = request.FILES['file']
        file_extension = file.name.split('.')[-1]

        # Read the file into a pandas DataFrame
        if file_extension == 'csv':
            df = pd.read_csv(file)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(file)
        else:
            return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

        candidates = []
        errors = []

        for index, row in df.iterrows():
            try:
                # Create a new user for each candidate

                # try creatinng a user with the email

                try:
                    user = get_user_model().objects.create_user(
                        username=row['email'],
                        password="0000",
                        email=row['email']
                    )
                except Exception as e:
                    user = get_user_model().objects.get(username=row['email'])


                candidate_data = {
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'nin': row.get('nin', ''),
                    'email': row['email'],
                    'phone': row.get('phone', ''),
                    'phone2': row.get('phone2', ''),
                    'photo': None,  # Assuming the photo field will be handled separately
                    'organisation_id': organisation,
                    'user': user.id
                }

                candidate_serializer = CandidateSerializer(data=candidate_data)
                if candidate_serializer.is_valid(raise_exception=True):
                    candidates.append(candidate_serializer.save())
            except Exception as e:
                errors.append({"row": index, "error": str(e)})

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": f"{len(candidates)} candidates created successfully."}, status=status.HTTP_201_CREATED)
    


class CandidateExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CandidateExam.objects.all()
    serializer_class = Candidate
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve a candidate exam
    def get(self, request, candidate_exam_id):
        candidate_exam = CandidateExam.objects.get(pk=candidate_exam_id)
        exam = candidate_exam.examination
        organisation_instance = exam.organisation
        # if user_is_staff_of_organization(request.user, organisation_instance) == False:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = CandidateExamSerializer(candidate_exam)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class DeactivateOrganisationAccount(generics.UpdateAPIView):
    queryset = Organisation.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    def put(self, request, organisation_id):
        organisation = Organisation.objects.get(pk=organisation_id)
        if  user_is_staff_of_organization(request.user, organisation) == False:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        organisation.active = False
        organisation.save()
        return Response(status=status.HTTP_200_OK)
    

