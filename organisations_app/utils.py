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
        all_objective = all(question.get('type') == 'objective' for question in questions)
        if not all_objective:
            raise ValidationError("All questions must be of type 'objective' for auto-grading.")
    
    validated_questions = []
    for question in questions:
        if 'score' not in question:
            question['score'] = 1  # Assign default score of 1 if not specified
        if 'id' not in question:
            question['id'] = str(uuid.uuid4())  # Assign a new UUID as id if not provided
        validated_questions.append(question)
    
    return validated_questions