from rest_framework import serializers
from .models import *
from organisations_app.models import *
from candidates_app.models import *
from admin_app.models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

