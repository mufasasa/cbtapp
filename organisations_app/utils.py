import random
import string


def generate_exam_number():
    """
    generate an alphanumeric exam number of length 6
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))