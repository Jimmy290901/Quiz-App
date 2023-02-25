from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

class Score(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=CASCADE)
    username = models.ForeignKey(User, on_delete=CASCADE)
    score = models.IntegerField(default=0)
    submitted = models.BooleanField(default=False)
