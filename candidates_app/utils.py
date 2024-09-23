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

        # update the candidate response dictionary
        candidate_exam.candidate_response_dict[question_id] = {'candidate_answer':candidate_answer,
                                                               'correct_answer':question_data.get('answer'),
                                                               'score':question_data.get('score')}

    # update the candidate exam with the total score
    candidate_exam.score = total_score
    candidate_exam.status = 'admitted'
    candidate_exam.save()

    return candidate_exam



def compute_exam_question_response_stats(exam:Examination) -> dict:
    """
    Compute the statistics of the exam questions based on the candidate responses
    """

    question_stats = defaultdict(dict)

    for question in exam.questions:
        question_id = question.get('id')
        question_stats[question_id]['question'] = question.get('question')
        question_stats[question_id]['options'] = question.get('options')
        question_stats[question_id]['correct_answer'] = question.get('answer')
        question_stats[question_id]['score'] = question.get('score')
        question_stats[question_id]['total_responses'] = 0
        question_stats[question_id]['correct_responses'] = 0
        question_stats[question_id]['incorrect_responses'] = 0

    # iterate through the candidate exams and update the stats
    for candidate_exam in CandidateExam.objects.filter(examination=exam):
        for question in candidate_exam.candidate_answers:
            question_id = question.get('id')
            candidate_answer = question.get('response')
            correct_answer = question_stats[question_id]['correct_answer']

            question_stats[question_id]['total_responses'] += 1

            if candidate_answer == correct_answer:
                question_stats[question_id]['correct_responses'] += 1
            else:
                question_stats[question_id]['incorrect_responses'] += 1

    return question_stats