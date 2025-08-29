from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_limit = models.IntegerField(help_text="Minutes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(choices=[(1,'Option1'),(2,'Option2'),(3,'Option3'),(4,'Option4')])

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name='attempts')
    score = models.FloatField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','quiz')  # one attempt per user per quiz

    def calculate_score(self):
        total_questions = self.answers.count()
        correct_answers = sum(
            1 for ans in self.answers.all() if ans.selected_option == ans.question.correct_option
        )
        self.score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        self.save()

class Answer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    selected_option = models.IntegerField()

    def is_correct(self):
        return self.selected_option == self.question.correct_option
