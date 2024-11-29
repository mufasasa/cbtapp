from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone


User = get_user_model()

EXAM_STATUS = (
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ('archived', 'Archived'),
)

COMPLAIN_STATUS = (
    ('not_attended', 'Not Attended'),
    ('waiting', 'Waiting'),
    ('cleared', 'Cleared'),
)


CANDIDATE_STATUS = (
    ('admitted', 'Admitted'),
    ('not_admitted', 'Not_admitted')
)



QUESTION_TYPE = (
    ('multiple_choice', 'Multiple Choice'),
    ('multiple_select', 'Multiple Select'),
    ('true_false', 'True False'),
    ('essay', 'Essay'),
    ('fill_in_the_blank', 'Fill in the Blank'),
)



class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class OrganisationAdmin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='admins')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    


class Examination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    total_marks = models.IntegerField(blank=True, null=True)
    passing_marks = models.IntegerField(blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='examinations')
    status = models.CharField(max_length=100, choices=EXAM_STATUS, default='draft')
    auto_grade = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_total_marks(self):
        return sum(question.marks for question in self.questions.all())

    def get_passing_marks(self):
        return self.passing_marks or 0

    def get_duration_in_minutes(self):
        return self.duration or 0

    def is_exam_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time if self.start_time and self.end_time else False
    
    def get_exam_analysis(self):
        from candidates_app.models import CandidateExam  # Import here to avoid circular import

        candidate_exams = CandidateExam.objects.filter(examination=self)
        total_candidates = candidate_exams.count()
        
        finished_exams = candidate_exams.filter(status='submitted')
        unfinished_exams = candidate_exams.exclude(status='submitted')
        
        passed_exams = finished_exams.filter(score__gte=self.passing_marks)
        failed_exams = finished_exams.filter(score__lt=self.passing_marks)
        
        total_score = sum(exam.score for exam in finished_exams if exam.score is not None)
        average_score = total_score / finished_exams.count() if finished_exams.count() > 0 else 0

        analysis = {
            'total_candidates': total_candidates,
            'finished_exams': finished_exams.count(),
            'unfinished_exams': unfinished_exams.count(),
            'passed_exams': passed_exams.count(),
            'failed_exams': failed_exams.count(),
            'average_score': round(average_score, 2)
        }

        return analysis
    



class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=100, choices=QUESTION_TYPE, default='multiple_choice')
    options = models.JSONField(default=list, blank=True, null=True)
    correct_answer = models.JSONField(default=dict)
    marks = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text[:50]

    def is_correct(self, answer):
        if self.question_type in ['multiple_choice', 'true_false']:
            return answer == self.correct_answer.get('answer')
        elif self.question_type == 'multiple_select':
            correct_answers = set(self.correct_answer.get('answers', []))
            given_answers = set(answer)
            return correct_answers == given_answers
        return False

    def get_correct_answer(self):
        if self.question_type in ['multiple_choice', 'true_false']:
            return self.correct_answer.get('answer')
        elif self.question_type == 'multiple_select':
            return self.correct_answer.get('answers', [])
        return None

    def set_correct_answer(self, answer):
        if self.question_type in ['multiple_choice', 'true_false']:
            self.correct_answer = {'answer': answer}
        elif self.question_type == 'multiple_select':
            self.correct_answer = {'answers': list(answer)}
        self.save()
    
    def get_question_analysis_report(self):
        from candidates_app.models import CandidateExam  # Import here to avoid circular import

        analysis = {
            'total_candidates': 0,
            'passed': 0,
            'failed': 0,
            'not_answered': 0,
            'passed_candidates': [],
            'failed_candidates': [],
            'not_answered_candidates': []
        }

        candidate_exams = CandidateExam.objects.filter(examination=self.examination)
        analysis['total_candidates'] = candidate_exams.count()

        for candidate_exam in candidate_exams:
            candidate_answer = CandidateAnswer.objects.filter(candidate=candidate_exam.candidate, question=self).first()
            
            if not candidate_answer:
                analysis['not_answered'] += 1
                analysis['not_answered_candidates'].append(str(candidate_exam.candidate.id))
            elif candidate_answer.is_correct:
                analysis['passed'] += 1
                analysis['passed_candidates'].append(str(candidate_exam.candidate.id))
            else:
                analysis['failed'] += 1
                analysis['failed_candidates'].append(str(candidate_exam.candidate.id))

        return analysis




class CandidateAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey('candidates_app.Candidate', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.JSONField(default=dict, blank=True, null=True)
    score = models.PositiveIntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.first_name} - {self.question.question_text[:50]}"

    def check_answer(self):
        self.is_correct = self.question.is_correct(self.answer)
        self.save()

    def mark_multiple_choice(self):
        if self.question.question_type == 'multiple_choice':
            self.is_correct = self.answer == self.question.get_correct_answer()
            self.score = self.question.marks if self.is_correct else 0
            self.save()

    def mark_multiple_select(self):
        if self.question.question_type == 'multiple_select':
            correct_answers = set(self.question.get_correct_answer())
            given_answers = set(self.answer)
            self.is_correct = correct_answers == given_answers
            self.score = self.question.marks if self.is_correct else 0
            self.save()

    def mark_essay(self, assigned_score):
        if self.question.question_type == 'essay':
            self.score = min(assigned_score, self.question.marks)
            self.is_correct = self.score > 0
            self.save()

    def mark_fill_in_the_blank(self):
        if self.question.question_type == 'fill_in_the_blank':
            correct_answer = self.question.get_correct_answer()
            given_answer = self.answer.get('answer', '').strip().lower()
            
            # Compare the given answer with the correct answer (case-insensitive)
            self.is_correct = given_answer == correct_answer.strip().lower()
            self.score = self.question.marks if self.is_correct else 0
            self.save()

    
    
    



class OrganisationComplain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='complains')
    topic = models.CharField(max_length=100)
    message = models.TextField()
    messages = models.JSONField(default=list, blank=True, null=True)
    status =  models.CharField(max_length=100, choices=COMPLAIN_STATUS, default='not_attended')
    created_at = models.DateTimeField(auto_now_add=True)
    admin  = models.ForeignKey(OrganisationAdmin, on_delete=models.CASCADE, related_name='complains')
    def __str__(self):
        return self.message
    

class CandidateExam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey('candidates_app.Candidate', on_delete=models.CASCADE, related_name='candidate_exams')
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='candidate_exams')
    exam_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CANDIDATE_STATUS, default='not_admitted')
    score = models.PositiveIntegerField(null=True, blank=True)
    admitted_by = models.CharField(max_length=200, blank=True, null=True)
    time_admitted = models.DateTimeField(null=True, blank=True)
    exam_end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.candidate.first_name} - {self.examination.name}"

    def get_answers(self):
        return CandidateAnswer.objects.filter(candidate=self.candidate, question__examination=self.examination)

    def calculate_score(self):
        total_score = 0
        for answer in self.get_answers():
            if answer.question.question_type == 'essay':
                # For essay questions, use the assigned score
                total_score += answer.score
            else:
                # For other question types, use the answer's score
                total_score += answer.score
        self.score = total_score
        self.save()

    def admit_candidate(self, admitted_by):
        self.status = 'admitted'
        self.admitted_by = admitted_by
        self.time_admitted = timezone.now()
        self.save()

    
    def auto_grade_exam(self):
        if self.examination.auto_grade:
            auto_gradable_types = ['multiple_choice', 'multiple_select', 'fill_in_the_blank']
            all_questions:list[Question] = self.examination.questions.all()
            
            if all(question.question_type in auto_gradable_types for question in all_questions):
                total_score = 0
                for question in all_questions:
                    answer = CandidateAnswer.objects.filter(candidate=self.candidate, question=question).first()
                    if answer:
                        if question.question_type == 'multiple_choice':
                            answer.mark_multiple_choice()
                            total_score += answer.score
                        elif question.question_type == 'multiple_select':
                            answer.mark_multiple_select()
                            total_score += answer.score
                        elif question.question_type == 'fill_in_the_blank':
                            answer.mark_fill_in_the_blank()
                            total_score += answer.score
                        else:
                            answer.score = 0
                        answer.save()
                
                self.score = total_score
                self.save()
                return True
        return False
    
    def extend_exam_time(self, additional_time):
        if self.exam_end_time:
            self.exam_end_time += timedelta(minutes=additional_time)
        else:
            self.exam_end_time = self.examination.end_time + timedelta(minutes=additional_time)
        self.save()
        return True
    

    def get_analysis_report(self):
        report = {
            'candidate_score': self.score,
            'questions_answered': [],
            'questions_unanswered': [],
            'total_questions': self.examination.questions.all().count(),
            'passed': False,
            'pass_marks': self.examination.passing_marks
        }

        for question in self.examination.questions.all():
            answer = CandidateAnswer.objects.filter(candidate=self.candidate, question__id=question['id']).first()
            if answer:
                report['questions_answered'].append({
                    'question_id': question['id'],
                    'score': answer.score,
                    'max_score': question['marks']
                })
            else:
                report['questions_unanswered'].append(question['id'])

        report['total_answered'] = len(report['questions_answered'])
        report['total_unanswered'] = len(report['questions_unanswered'])

        if self.score is not None and self.examination.total_marks > 0:
            score_percentage = (self.score / self.examination.total_marks) * 100
            report['passed'] = score_percentage >= self.examination.passing_marks

        # Get overall exam statistics
        all_candidate_exams = CandidateExam.objects.filter(examination=self.examination)
        total_candidates = all_candidate_exams.count()
        passed_candidates = all_candidate_exams.filter(score__gte=self.examination.passing_marks).count()
        failed_candidates = total_candidates - passed_candidates

        report['exam_statistics'] = {
            'total_candidates': total_candidates,
            'passed_candidates': passed_candidates,
            'failed_candidates': failed_candidates,
            'pass_rate': (passed_candidates / total_candidates * 100) if total_candidates > 0 else 0
        }

        return report
    
    