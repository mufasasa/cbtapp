import datetime
from django.shortcuts import render
from .models import *
from organisations_app.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# from authentication.models import TimedAuthToken
from authentication.authentication import TimedAuthTokenAuthentication
from organisations_app.serializers import *
from rest_framework.pagination import PageNumberPagination



class OrganisationAdminListCreateView(generics.ListCreateAPIView):
    queryset = OrganisationAdmin.objects.all()
    serializer_class = OrganisationAdminSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # list all organisation admins
    def get(self, request):
        organisation_admins = OrganisationAdmin.objects.all()
        serializer = OrganisationAdminSerializer(organisation_admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new organisation admin
    def post(self, request):
        serializer = OrganisationAdminSerializer(data=request.data)
        # if no user exists with email
        # create a new user
        User = get_user_model()
        if User.objects.filter(username=request.data['email']).exists():
            user = User.objects.get(username=request.data['email'])
        else:
            user = get_user_model().objects.create_user(
                username=request.data['email'],
                password=request.data['password'],
                email=request.data['email']
            )

        # create a new organisation admin
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class OrganisationAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganisationAdmin.objects.all()
    serializer_class = OrganisationAdminSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve an organisation admin
    def get(self, request, pk):
        organisation_admin = OrganisationAdmin.objects.get(pk=pk)
        serializer = OrganisationAdminSerializer(organisation_admin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update an organisation admin
    def put(self, request, pk):
        organisation_admin = OrganisationAdmin.objects.get(pk=pk)
        serializer = OrganisationAdminSerializer(organisation_admin, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # delete an organisation admin
    def delete(self, request, pk):
        organisation_admin = OrganisationAdmin.objects.get(pk=pk)
        organisation_admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




class SuperAdminListCreateView(generics.ListCreateAPIView):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TimedAuthTokenAuthentication]

    # list all super admins
    def get(self, request):
        super_admins = SuperAdmin.objects.all()
        serializer = SuperAdminSerializer(super_admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new super admin
    def post(self, request):

        # create a new user
        user = get_user_model().objects.create_user(
            username=request.data['email'],
            password=request.data['password'],
            email=request.data['email']
        )

        # create a new super admin
        super_admin = SuperAdmin.objects.create(
            user=user,
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email']
        )

        super_admin.save()

        return Response(
            {
                'id': str(super_admin.id),
                'first_name': super_admin.first_name,
                'last_name': super_admin.last_name,
                'email': super_admin.email
            }, 
            status=status.HTTP_201_CREATED
        )


class SuperAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve a super admin
    def get(self, request, pk):
        super_admin = SuperAdmin.objects.get(pk=pk)
        serializer = SuperAdminSerializer(super_admin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a super admin
    def put(self, request, pk):
        super_admin = SuperAdmin.objects.get(pk=pk)
        serializer = SuperAdminSerializer(super_admin, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # delete a super admin
    def delete(self, request, pk):
        super_admin = SuperAdmin.objects.get(pk=pk)
        super_admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ReceptionStaffListCreateView(generics.ListCreateAPIView):
    queryset = ReceptionStaff.objects.all()
    serializer_class = ReceptionStaffSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # list all reception staff
    def get(self, request):
        reception_staff = ReceptionStaff.objects.all()
        serializer = ReceptionStaffSerializer(reception_staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new reception staff
    def post(self, request):
        #make a copy of the data and create a user to add  to the reception staff
        mutable = request.data.copy()
        user = get_user_model().objects.create_user(
            username=request.data['email'],
            password=request.data['password'],
            email=request.data['email']
        )
        mutable['user'] = user.id
        serializer = ReceptionStaffSerializer(data=mutable)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReceptionStaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReceptionStaff.objects.all()
    serializer_class = ReceptionStaffSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve a reception staff
    def get(self, request, pk):
        reception_staff = ReceptionStaff.objects.get(pk=pk)
        serializer = ReceptionStaffSerializer(reception_staff)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a reception staff
    def put(self, request, pk):
        reception_staff = ReceptionStaff.objects.get(pk=pk)
        serializer = ReceptionStaffSerializer(reception_staff, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # delete a reception staff
    def delete(self, request, pk):
        reception_staff = ReceptionStaff.objects.get(pk=pk)
        reception_staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class SuperAdminListAllOrganisationsView(generics.ListAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]
    paginator = PageNumberPagination()

    # list all organisations
    def get(self, request):
        organisations = Organisation.objects.all()
        page = self.paginate_queryset(organisations)
        if page is not None:
            serializer = OrganisationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SuperAdminActivateOrganisationView(generics.UpdateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # activate an organisation
    def put(self, request, organisation_id):
        organisation = Organisation.objects.get(id=organisation_id)
        organisation.active = True
        organisation.save()
        return Response(status=status.HTTP_200_OK)
    

class SuperAdminDeactivateOrganisationView(generics.UpdateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # deactivate an organisation
    def put(self, request, organisation_id):
        organisation = Organisation.objects.get(id=organisation_id)
        organisation.active = False
        organisation.save()
        return Response(status=status.HTTP_200_OK)
    


class SuperAdminGetAllComplainsView(generics.ListAPIView):
    queryset = OrganisationComplain.objects.all()
    serializer_class = OrganisationComplainSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]
    paginator = PageNumberPagination()

    # list all complains
    def get(self, request):
        complains = OrganisationComplain.objects.all()
        # filters: organisation, status; not_attended, waiting, cleared
        if request.query_params.get('organisation'):
            complains = complains.filter(organisation=request.query_params.get('organisation'))
        if request.query_params.get('status'):
            complains = complains.filter(status=request.query_params.get('status'))

        page = self.paginate_queryset(complains)
        if page is not None:
            serializer = OrganisationComplainSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrganisationComplainSerializer(complains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SuperAdminGetComplainView(generics.RetrieveUpdateAPIView):

    queryset = OrganisationComplain.objects.all()
    serializer_class = OrganisationComplainSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # retrieve a complain
    def get(self, request, complain_id):
        complain = OrganisationComplain.objects.get(id=complain_id)
        serializer = OrganisationComplainSerializer(complain)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a complain status
    def put(self, request, complain_id):
        complain = OrganisationComplain.objects.get(id=complain_id)
        complain.status = request.data['status']
        complain.save()
        return Response(status=status.HTTP_200_OK)
    


class VisitorListCreateView(generics.ListCreateAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [AllowAny]
    paginator = PageNumberPagination()


    # list all visitors
    def get(self, request):
        visitors = Visitor.objects.all()
        if request.query_params.get('date'):
            visitors = Visitor.objects.filter(created_at=request.query_params.get('date'))

        page = self.paginate_queryset(visitors)
        if page is not None:
            serializer = VisitorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = VisitorSerializer(visitors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # create a new visitor
    def post(self, request):
        serializer = VisitorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VisitorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [AllowAny]

    # retrieve a visitor
    def get(self, request, visitor_id):
        visitor = Visitor.objects.get(id=visitor_id)
        serializer = VisitorSerializer(visitor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # update a visitor
    def put(self, request, visitor_id):
        visitor = Visitor.objects.get(id=visitor_id)
        serializer = VisitorSerializer(visitor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # delete a visitor
    def delete(self, request, visitor_id):
        visitor = Visitor.objects.get(id=visitor_id)
        visitor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class AdminReplyOrganisationComplainView(generics.UpdateAPIView):
    queryset = OrganisationComplain.objects.all()
    serializer_class = OrganisationComplainSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # reply to a complain
    def put(self, request, complain_id):
        complain = OrganisationComplain.objects.get(id=complain_id)
        messages:list = complain.messages
        # fetch the message  from the request
        message = request.data['message']

        # create a message object with the username of the sender  and date
        messages.append({
            'message': message,
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': str(request.user.id),
            'sender_username': request.user.username
        })
        complain.messages = messages
        if complain.status == 'not_attended':
            complain.status = 'waiting'
        complain.save()
        return Response(status=status.HTTP_200_OK)
    

class AdminMarkComplainClearedView(generics.UpdateAPIView):
    queryset = OrganisationComplain.objects.all()
    serializer_class = OrganisationComplainSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    # mark a complain as cleared
    def put(self, request, complain_id):
        complain = OrganisationComplain.objects.get(id=complain_id)
        complain.status = 'cleared'
        complain.save()
        return Response(status=status.HTTP_200_OK)
    


class AdminGetAllExamsView(generics.RetrieveAPIView):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]
    paginator = PageNumberPagination()

    # retrieve all exams
    def get(self, request):
        exams = Examination.objects.all()

        # filters: organisation, date
        if request.query_params.get('organisation'):
            exams = exams.filter(organisation=request.query_params.get('organisation'))
        if request.query_params.get('date'):
            # filter for only  date though, in the start_time time not included
            exams = exams.filter(start_time__date=request.query_params.get('date'))

        page = self.paginate_queryset(exams)
        if page is not None:
            serializer = ExaminationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ExaminationSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AdminGetAllExamCandidates(generics.RetrieveAPIView):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]
    paginator = PageNumberPagination()

    # retrieve all exam candidates

    def get(self, request, *args, **kwargs):
        
        all_candidates = CandidateExam.objects.all()

        # filters: exam, organisation, date, status

        if request.query_params.get('exam'):
            all_candidates = all_candidates.filter(examination=request.query_params.get('exam'))

        if request.query_params.get('organisation'):
            all_candidates = all_candidates.filter(examination__organisation=request.query_params.get('organisation'))

        if request.query_params.get('date'):
            all_candidates = all_candidates.filter(examination__start_time=request.query_params.get('date'))

        if request.query_params.get('status'):
            all_candidates = all_candidates.filter(status=request.query_params.get('status'))

        page = self.paginate_queryset(all_candidates)
        if page is not None:
            serializer = CandidateExamSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CandidateExamSerializer(all_candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AdminMarkCandidateAdmittedView(generics.UpdateAPIView):
    """
    This view marks the status on a candidate exam as admitted
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    def update(self, request, candidate_exam_id):

        # get the candidate_exam
        candidate_exam_instance = CandidateExam.objects.get(id=candidate_exam_id)

        candidate_exam_instance.status = 'admitted'
        candidate_exam_instance.admitted_by =  request.user.username
        candidate_exam_instance.time_admitted = datetime.datetime.now()
        candidate_exam_instance.save()

        return Response({'message':'successfully admitted'}, status=status.HTTP_200_OK)
    

        

class ExitVisitorView(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TimedAuthTokenAuthentication]

    def update(self, request, visitor_id):

        # get the visitor
        visitor_instance = Visitor.objects.get(id=visitor_id)

        visitor_instance.exited = True
        visitor_instance.time_of_exit = datetime.datetime.now()
        visitor_instance.save()

        return Response({'message':'successfully exited'}, status=status.HTTP_200_OK)