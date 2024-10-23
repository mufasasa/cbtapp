import random
import string
from rest_framework.exceptions import ValidationError
from organisations_app.models import Question
import uuid


def generate_exam_number():
    """
    generate an alphanumeric exam number of length 6
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))



def validate_questions(questions, auto_grade=False):
    if auto_grade:
        all_objective = all(question.get('question_type') in ['multiple_choice', 'true_false', 'multiple_select'] for question in questions)
        if not all_objective:
            raise ValidationError("All questions must be of type 'objective' for auto-grading.")
    
    validated_questions = []
    for question in questions:
        if 'score' not in question:
            question['score'] = 1  # Assign default score of 1 if not specified
        validated_questions.append(question)
        
    return validated_questions


def update_questions(questions:list[dict]):
    for question in questions:
        try:    
            question_obj = Question.objects.get(pk=question['id'])
            question_obj.question_text = question['question_text'] if 'question_text' in question else question_obj.question_text
            question_obj.options = question['options'] if 'options' in question else question_obj.options
            question_obj.marks = question['score'] if 'score' in question else question_obj.marks
            question_obj.save()
        except Question.DoesNotExist:
            raise ValidationError(f"Question with id {question['id']} does not exist")
    return questions