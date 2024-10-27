from django.db import models
from django.contrib.auth.models import User
from authentication.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_user': True})
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:30]  # Return first 30 characters as title


class Answer(models.Model):
    comment = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_owner': True})
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commented by {self.author} on {self.comment}"
