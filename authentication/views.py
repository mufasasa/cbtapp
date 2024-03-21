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
            user = get_user_model().objects.filter(username=request.data['username'])
            if not user.exists():
                return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
            user = user.first()
            # validate the password
            if not user.check_password(request.data['password']):
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            
            token, created = TimedAuthToken.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
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
