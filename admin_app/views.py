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
from organisations_app.serializers import OrganisationSerializer




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

        # create a new user
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
        serializer = ReceptionStaffSerializer(data=request.data)

        # create a new user
        user = get_user_model().objects.create_user(
            username=request.data['email'],
            password=request.data['password'],
            email=request.data['email']
        )

        # create a new reception staff
        if serializer.is_valid():
            serializer.save(user=user)
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

    # list all organisations
    def get(self, request):
        organisations = Organisation.objects.all()
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