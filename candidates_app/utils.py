from  organisations_app.models import CandidateExam,  Examination
from collections import defaultdict




def auto_grade_exam(candidate_exam:CandidateExam, examination:Examination) -> CandidateExam:

    # form a dictionary of question ids with answers and scores.

    question_id_score_answer_dict = {}

    for question in examination.questions:
        question_id = question.get('id')
        question_score = question.get('score')
        question_answer =  question.get('answer')

        data = {'score':question_score, 'answer':question_answer}

        question_id_score_answer_dict[question_id] = data

    
    # mark the exam
    total_score = 0
    for question in candidate_exam.candidate_answers:
        question_id = question.get('id')
        candidate_answer = question.get('response')

        question_data = question_id_score_answer_dict.get(question_id)

        if question_data.get('answer') == candidate_answer:
            total_score += question_data.get('score')

    # update the candidate exam with the total score
    candidate_exam.score = total_score
    candidate_exam.status = 'admitted'
    candidate_exam.save()

    return candidate_exam