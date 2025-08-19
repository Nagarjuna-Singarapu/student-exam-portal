from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text[:40]} ({'Correct' if self.is_correct else 'Wrong'})"

class ExamAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    total_questions = models.IntegerField(default=0)
    duration_seconds = models.IntegerField(default=1800)
    questions_snapshot = models.JSONField(default=dict)   # {"ids": [1,2,3]}
    answers = models.JSONField(null=True, blank=True)     # {"1": 4, "2": 7}

    def __str__(self):
        return f"Attempt {self.id} by {self.user}"
