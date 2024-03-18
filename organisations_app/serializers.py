from rest_framework import serializers
from .models import *
from candidates_app.models import *





class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'