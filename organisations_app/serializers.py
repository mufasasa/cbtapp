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


class ExaminationDetailSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True)
    
    class Meta:
        model = Examination
        fields = '__all__'


class CreateExamSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    duration = serializers.IntegerField(required=False)
    instructions = serializers.CharField(required=False)
    total_marks = serializers.IntegerField(required=False)
    passing_marks = serializers.IntegerField(required=False)
    questions = serializers.ListField(child=serializers.DictField(), required=False, allow_empty=True)
    candidates = serializers.ListField(child=serializers.UUIDField(), required=False, allow_empty=True)
    organisation = serializers.UUIDField()

    def create(self, validated_data):
        organisation = Organisation.objects.get(pk=validated_data['organisation'])
        exam = Examination.objects.create(
            name=validated_data['name'],
            description=validated_data['description'] if 'description' in validated_data else None,
            start_time=validated_data['start_time'] if 'start_time' in validated_data else None,
            end_time=validated_data['end_time'] if 'end_time' in validated_data else None,
            duration=validated_data['duration'] if 'duration' in validated_data else None,
            instructions=validated_data['instructions'] if 'instructions' in validated_data else None,
            questions=validated_data.get('questions', []),
            total_marks=validated_data['total_marks'] if 'total_marks' in validated_data else None,
            passing_marks=validated_data['passing_marks'] if 'passing_marks' in validated_data else None,
            organisation=organisation
        )
        # add the candidates, which is a many to many field
        if 'candidates' in validated_data:
            for candidate_id in validated_data['candidates']:
                candidate = Candidate.objects.get(pk=candidate_id)
                exam.candidates.add(candidate)
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

class OrganisationCreateCandidateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    nin = serializers.CharField()
    email = serializers.EmailField()
    phone_number_1 = serializers.CharField()
    phone_number_2 = serializers.CharField(required=False)


class OrganisationComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationComplain
        fields = '__all__'