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


class ExaminationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class CreateExamSerializer(serializers.ModelSerializer):
    candidates = serializers.ListField(child=serializers.UUIDField(), required=False, allow_empty=True, write_only=True)
    questions = ExaminationQuestionSerializer(many=True, required=False, allow_empty=True)

    class Meta:
        model = Examination
        fields = ['name', 'description', 'start_time', 'end_time', 'duration', 'instructions', 
                  'total_marks', 'passing_marks', 'questions', 'candidates', 'organisation', 'auto_grade']
        extra_kwargs = {
            'description': {'required': False},
            'duration': {'required': False},
            'instructions': {'required': False},
            'total_marks': {'required': False},
            'passing_marks': {'required': False},
            'auto_grade': {'required': False, 'default': True},
        }

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        
        exam = Examination.objects.create(**validated_data)
        
        for question_data in questions_data:
            Question.objects.create(
                examination=exam,
                question_text=question_data.get('question_text'),
                question_type=question_data.get('question_type', 'multiple_choice'),
                options=question_data.get('options', []),
                correct_answer=question_data.get('correct_answer', {}),
                marks=question_data.get('score', 1)
            )
        exam.save()
        return exam
    
    def validate(self, data):
        if data.get('auto_grade'):
            all_objective = all(question.get('question_type') in ['multiple_choice', 'true_false', 'multiple_select'] for question in data.get('questions', []))
            if not all_objective:
                raise serializers.ValidationError("All questions must be of type 'multiple_choice', 'true_false' or 'multiple_select' for auto-grading.")

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
