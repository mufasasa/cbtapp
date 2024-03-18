from rest_framework import serializers
from .models import *


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class OrganisationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationAdmin
        fields = '__all__'


class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = '__all__'


class ReceptionStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptionStaff
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'