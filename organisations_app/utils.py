import random
import string
from rest_framework.exceptions import ValidationError
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