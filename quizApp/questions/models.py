from django.db import models
from django.db.models.deletion import CASCADE
from quiz.models import Quiz

# Create your models here.

class MCQ(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=CASCADE)
    question_text = models.TextField()
    image = models.ImageField(upload_to = 'Questions_Images', blank = True, null = True)
    total_options = models.IntegerField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField(null=True, blank = True)
    option4 = models.TextField(null = True, blank = True)
    correct_option_number = models.IntegerField()

class Textual(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=CASCADE)
    question_text = models.TextField()
    image = models.ImageField(upload_to = 'Questions_Images', blank = True, null = True)
    answer_text = models.TextField()
