import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from company.models import Company, Question,  Test_generation, UserAnswer, test_score, test_shortlist
from company.views import parsing
from student.models import Application_Student, Student_Register
from django.contrib.auth import authenticate, login
import csv
import re
import spacy
from django.core.files.storage import FileSystemStorage
import pandas as pd
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from bs4 import BeautifulSoup
import urllib.request
import numpy as np
from django.conf import Settings, settings
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
# Create your views here.
def home(request):
    return render(request, 'student/registration1.html')

def register_stud(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        s = Student_Register()
        s.name = name
        s.email = email
        s.phone = phone
        s.password = password
        s.save()
        return render(request, 'student/home.html', {'message': True, 'id':name, 'test': False})
    else:
        return render(request, 'student/registration.html') 
    

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = Student_Register.objects.filter(email=email, password=password).first()
        if user is not None:
            return render(request, 'student/home.html', {'message': True, 'id':user.name, 'test': False})
        else:
            return render(request, 'student/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'student/login.html')


def application(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['resume']
        fs = FileSystemStorage()
        folder_name = 'uploads'
        folder_path = os.path.join(settings.BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        filename = fs.save(os.path.join(folder_name, uploaded_file.name), uploaded_file)
        uploaded_file_url = fs.url(filename)
        ans1 = parsing(uploaded_file_url)
        name=request.POST.get('name')
        email  = request.POST.get('email')
        date = request.POST.get('date')
        gender=request.POST.get('gender')
        phone=request.POST.get('phone')
        strengths=request.POST .get('strengths')
        weakness=request.POST.get('weakness')
        ap = Application_Student()
        ap.name = name
        ap.email  = email
        ap.date = date
        ap.gender = gender
        ap.phone = phone
        ap.strengths = strengths
        ap.weakness = weakness
        ap.resume = uploaded_file_url
        ap.skills = ans1
        ap.save()
        return render(request, 'student/application.html', {'error': True})
       
    else:
            return render(request, 'student/application.html')
    



   

def test(request):
    count = Test_generation.objects.count()
    if count ==0:
        return HttpResponse("not found")
    record = Test_generation.objects.all().values()
    option_values = []

    for record in record:
        option_value = record['option']
        option_values.append(option_value)
    val = option_values
    print(val[0])
    # context={'category':val[0]}
    # # context={'category':request.GET.get('category')}
    # print("Hello")
    # print(context)
    if val[0]==True:
        questions = Question.objects.all()
   
        context = {'questions': questions}
        print(context)
        return render(request,'student/quiz1.html',context)
    return HttpResponse("not found")


@login_required
def calculate_score(request):
    if request.method == 'POST':
        user = request.user
        questions = Question.objects.all()
        score = 0
        email = request.POST.get('email')
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}', None)
            if selected_choice_id:
                selected_choice = question.choice_set.get(id=selected_choice_id)
                UserAnswer.objects.create(user=user, question=question, selected_choice=selected_choice)
                if selected_choice.is_correct:
                    score += 1
        context = {'score': "Thank you"}
        print(email)
        s = test_score()
        s.email = email
        s.score = score
        s.save()
        print(score)
        return render(request, 'student/score.html',context)
    else:
        return HttpResponse("Hello")
       
# def calculate_score(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user_answers = UserAnswer.objects.all()  # Get all user answers
        
#         total_questions = user_answers.count()
#         correct_answers = user_answers.filter(selected_choice__is_correct=True).count()
#         print(correct_answers)
#         # incorrect_answers = total_questions - correct_answers
        
#         score = (correct_answers) 
#         # s = test_score()
#         # s.email = email
#         # s.score = score
#         # s.save()
#         print(score)
        
        
#         return render(request, 'student/score.html', {'score':score})
    
#     # return HttpResponse(score)