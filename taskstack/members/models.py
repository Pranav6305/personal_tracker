from django.db import models
from django.utils import timezone

class Signup(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'members_signup'

    def __str__(self):
        return self.username

from django.db import models

class Task(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)  # ✅ Add this line
    updated_at = models.DateTimeField(auto_now=True)

    def mark_completed(self):
        self.is_completed = True
        self.completion_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} ({'Done' if self.is_completed else 'Pending'})"

