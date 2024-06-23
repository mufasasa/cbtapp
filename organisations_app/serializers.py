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
            description=validated_data.get('description'),
            start_time=validated_data.get('start_time'),
            end_time=validated_data.get('end_time'),
            duration=validated_data.get('duration'),
            instructions=validated_data.get('instructions'),
            questions=validated_data.get('questions', []),
            total_marks=validated_data.get('total_marks'),
            passing_marks=validated_data.get('passing_marks'),
            organisation=organisation,
            auto_grade=validated_data.get('auto_grade', False)
        )
        if 'candidates' in validated_data:
            for candidate_id in validated_data['candidates']:
                candidate = Candidate.objects.get(pk=candidate_id)
                exam.candidates.add(candidate)
        return exam
    
    def validate(self, data):
        if data.get('auto_grade'):
            all_objective = all(question.get('type') == 'objective' for question in data.get('questions', []))
            if not all_objective:
                raise serializers.ValidationError("All questions must be of type 'objective' for auto-grading.")

        questions = []
        for question in data.get('questions', []):
            if 'score' not in question:
                question['score'] = 1  # Assign default score of 1 if not specified
            if 'id' not in question:
                question['id'] = str(uuid.uuid4())  # Assign a new UUID as id if not provided
            questions.append(question)
        
        data['questions'] = questions
        return data

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




class CandidateExamSerializer(serializers.ModelSerializer):
    first_name =  serializers.SerializerMethodField()
    last_name =  serializers.SerializerMethodField()
    nin =  serializers.SerializerMethodField()
    email =  serializers.SerializerMethodField()
    exam_number =  serializers.SerializerMethodField()
    exam_name = serializers.SerializerMethodField()

    class Meta:
        model = CandidateExam
        fields = '__all__'

    def get_first_name(self, obj):
        return obj.candidate.first_name
    
    def get_last_name(self, obj):
        return obj.candidate.last_name
    
    def get_nin(self, obj):
        return obj.candidate.nin
    
    def get_email(self, obj):
        return obj.candidate.email
    
    def get_exam_number(self, obj):
        return obj.exam_number
    
    def get_exam_name(self, obj):
        return obj.examination.name
    


class CandidateUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
