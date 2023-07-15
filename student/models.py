from django.db import models

# Create your models here.
class Student_Register(models.Model): 
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone=models.CharField(max_length=12) 
    password=models.CharField(max_length=20)

def upload_to( inst, filename ):
    return "/profile/"+str(filename)

class Application_Student(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=125)
    date = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=10)
    phone=models.CharField(max_length=12)
    strengths=models.CharField(max_length=100)
    weakness=models.CharField(max_length=100)
    resume=models.FileField(upload_to='uploads/')
    skills = models.CharField(max_length=150,default = "none")


