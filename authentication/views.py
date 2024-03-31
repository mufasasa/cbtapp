from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from django.contrib.auth import get_user_model
from .serializers import *
from authentication.authentication import *





class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    # login a user
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = get_user_model().objects.filter(username=request.data['email'])
            if not user.exists():
                return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
            user = user.first()
            # validate the password
            if not user.check_password(request.data['password']):
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            
            # get organisation admins, super admins and reception staff attached to the user
            organisation_admin = OrganisationAdmin.objects.filter(user=user)
            super_admin = SuperAdmin.objects.filter(user=user)
            reception_staff = ReceptionStaff.objects.filter(user=user)

            # list of entities the user is attached to with ids, names and organisation ids
            entities = {}

            # organisation admins
            organisation_admins = []
            for org_admin in organisation_admin:
                organisation_admins.append({
                    'id': str(org_admin.id),
                    'name': org_admin.first_name + ' ' + org_admin.last_name,
                    'organisation_id': str(org_admin.organisation.id),
                    'entity': 'organisation_admin',
                    'organisation_name': org_admin.organisation.name
                })
            
            # super admins
            super_admins = []
            for s_admin in super_admin:
                super_admins.append({
                    'id': str(s_admin.id),
                    'name': s_admin.first_name + ' ' + s_admin.last_name,
                    'entity': 'super_admin'
                })
            
            # reception staff
            reception_staffs = []
            for r_staff in reception_staff:
                reception_staffs.append({
                    'id': str(r_staff.id),
                    'name': r_staff.first_name + ' ' + r_staff.last_name,
                    'entity': 'reception_staff'
                })

            entities['organisation_admins'] = organisation_admins
            entities['super_admins'] = super_admins
            entities['reception_staffs'] = reception_staffs


            
            
            token = TimedAuthToken.objects.create(user=user)
            return Response({'token': token.key, 'entities':entities}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ResetPasswordView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TimedAuthTokenAuthentication]

    # reset the password of a user
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = get_user_model().objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
