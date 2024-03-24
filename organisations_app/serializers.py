from rest_framework import serializers
from .models import *
from candidates_app.models import *
from organisations_app.models import *





class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'




class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = '__all__'


class CreateExamSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    duration = serializers.DurationField()
    instructions = serializers.CharField()
    total_marks = serializers.IntegerField()
    passing_marks = serializers.IntegerField()
    questions = serializers.ListField(child=serializers.DictField())
    candidates = serializers.ListField(child=serializers.UUIDField(), required=False, allow_empty=True)
    organisation = serializers.UUIDField()

    def create(self, validated_data):
        exam = Examination.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            duration=validated_data['duration'],
            instructions=validated_data['instructions'],
            questions=validated_data['questions'],
            total_marks=validated_data['total_marks'],
            passing_marks=validated_data['passing_marks'],
            organisation=Organisation.objects.get(pk=validated_data['organisation'])
        )

        for candidate in validated_data['candidates']:
            exam.candidates.add(Candidate.objects.get(pk=candidate))

        return exam
    

class OrganisationCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    website = serializers.URLField(required=False)
    logo = serializers.ImageField(required=False)

    

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'
