from rest_framework import serializers
from .models import *
from organisations_app.models import *




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
