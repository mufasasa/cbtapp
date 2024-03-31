from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.authentication import TimedAuthTokenAuthentication
from authentication.utils  import user_is_in_entity, get_user_entity_instance, user_is_staff_of_organization
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *




class UploadFileView(generics.CreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            file_instance = FileUpload.objects.create(
                file = request.data['file'],
                user = request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FileDownLoadView(generics.RetrieveAPIView):
    queryset = FileUpload.objects.all()
    

    def get(self, request, file_id):
        file = FileUpload.objects.get(id=file_id)
        file_path = file.file.url
        return Response({'file_path': file_path}, status=status.HTTP_200_OK)
        