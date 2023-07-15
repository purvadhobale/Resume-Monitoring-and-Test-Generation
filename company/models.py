import random
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=125)
    email = models.EmailField(max_length=125)
    password = models.CharField(max_length=10)

class ShortList(models.Model):
    id1 = models.IntegerField()
    name = models.CharField(max_length=125)
    email=models.EmailField(max_length=125)
    phone = models.CharField(max_length=10)
    skills = models.CharField(max_length=125)

class category(models.Model):
      category_name=models.CharField(max_length=100)

      def __str__(self) -> str:
            return self.category_name
      
class Test_generation(models.Model):
     category = models.CharField(max_length=125)
     option = models.BooleanField(default=False)

class Question(models.Model):

    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class UserAnswer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.question}"
    
class test_shortlist(models.Model):
    email = models.EmailField(max_length=125)
    score= models.IntegerField(default=0)

class test_score(models.Model):
    email = models.EmailField(max_length=125)
    score = models.IntegerField(default=0)

class final_shortlist(models.Model):
    email = models.EmailField(max_length=125)