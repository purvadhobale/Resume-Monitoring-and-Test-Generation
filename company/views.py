import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
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
from company.models import *
from student.models import Application_Student

# Create your views here.

def company_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        s = Company()
        s.name = name
        s.email = email
        s.password = password
        s.save()
        return render(request, 'company/home1.html',{'name': name})
    else:
        return render(request, 'company/register.html')
def login_company(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Company.objects.filter(email=email, password=password).first()
        if user is not None:
            return redirect('/company/home/')
        else:
            return render(request, 'company/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'company/login.html')
    
def home(request):
    resumes = Application_Student.objects.all().values()
    return render(request, 'company/home1.html', {'resume': resumes})

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def extract_name(string):
    r1 = string
    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(r1)
    for ent in doc.ents:
        if ent.label_ == 'PER':
            print(ent.text)
            break

def extract_phone_numbers(string):
    r = re.compile(
        r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

# Converting pdf to string

# resume_string = convert(r"uploads\uploads\Purva_Dhobale.pdf")

# resume_string1 = resume_string
# # Removing commas in the resume for an effecient check
# resume_string = resume_string.replace(',', ' ')
# # Converting all the charachters in lower case
# resume_string = resume_string.lower()

# Information Extraction Function


def extract_information(string):
    soup = BeautifulSoup(urllib.request.urlopen(
        "https://en.wikipedia.org/wiki/" + string), "html.parser")
    # creates soup and opens URL for Google. Begins search with site:wikipedia.com so only wikipedia
    # links show up. Uses html parser.
    for item in soup.find_all('div', attrs={'id': "mw-content-text"}):
        print(item.find('p').get_text())
        print('\n')


file_path = os.path.join(os.path.dirname(__file__), 'techatt.csv')
file_path1 = os.path.join(os.path.dirname(__file__), 'techskill.csv')
file_path2 = os.path.join(os.path.dirname(__file__), 'nontechnicalskills.csv')

with open(file_path, 'r') as f:
    reader = csv.reader(f)
    your_listatt = list(reader)
with open(file_path1, 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)
with open(file_path2, 'r') as f:
    reader = csv.reader(f)
    your_list1 = list(reader)




def parsing(str):
    str1 = "uploads/" + str
    resume_string = convert(str1)

    resume_string1 = resume_string
    # Removing commas in the resume for an effecient check
    resume_string = resume_string.replace(',', ' ')
    # Converting all the charachters in lower case
    resume_string = resume_string.lower()
    s = set(your_list[0])
    s1 = your_list
    s2 = your_listatt
    skillindex = []
    skills = []
    skillsatt = []
    print('\n')
    print('Phone Number is')
    y = extract_phone_numbers(resume_string)
    y1 = []
    for i in range(len(y)):
        if (len(y[i]) > 9):
            y1.append(y[i])
    print(y1)
    print('\n')
    print('Email id is')
    print(extract_email_addresses(resume_string))
    for word in resume_string.split(" "):
        if word in s:
            skills.append(word)
    skills1 = list(set(skills))
    print('\n')
    print("Following are his/her Technical Skills")
    print('\n')
    np_a1 = np.array(your_list)
    for i in range(len(skills1)):
        item_index = np.where(np_a1 == skills1[i])
        skillindex.append(item_index[1][0])
    ans =[]
    nlen = len(skillindex)
    for i in range(nlen):
        print(skills1[i])
        ans.append(skills1[i])
        ans.append(',')
        print(s2[0][skillindex[i]])
        print('\n')
    
    # ans.append(y1)
    # ans.append(extract_email_addresses(resume_string))
    
    return ans


# def test_generate(request):
#     record = ShortList.objects.all().values()
#     return render(request, 'student/home.html',{'test':True, 'shortlist':record})

def sorting(request):
    indexs = []
    skill = request.POST.get('required')
    record = Application_Student.objects.all().values()
    
    for x in record:
        s = x['skills']
        print(s)
        if skill in s:
            indexs.append(x['id'])
            student = ShortList(id1=x['id'],name=x['name'],email=x['email'],phone=x['phone'],skills=x['skills'])
            student.save()
    shortlist = ShortList.objects.all().values()
    
    return render(request,'company/home1.html', {'message': True,'shortlist': shortlist})

def deleteshortlist(request):
    record = ShortList.objects.all()
    record.delete()
    return render(request,'company/home1.html')


def test_generate(request):
    context = {'categories':category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/company/quiz/?category=js")
    # #    return redirect(f"/company/quiz/?category={request.GET.get('category')}")

    return render(request,"company/category.html",context)

def deleteoption():
    record = Test_generation.objects.all()
    record.delete()
    


# def make_true(request):
    
#     if request.method == 'POST':
#         option = request.POST.get('option')
#         deleteoption()
#         s = Test_generation()
#         s.option = option
#         s.save()
#         return HttpResponse("done")
# @login_required
# def quiz(request):
#     # record = Test_generation.objects.all().values()
#     # option_values = []

#     # for record in record:
#     #     option_value = record['category']
#     #     option_values.append(option_value)
#     # val = option_values
#     # print(val[0])
#     # context={'category':val[0]}
#     # # context={'category':request.GET.get('category')}
#     # print("Hello")
#     # print(context)
#     questions = Question.objects.all()
   
#     context = {'questions': questions}
#     print(context)
#     return context
    # return render(request,'company/quiz.html',context)
 
def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        if request.GET.get('category'):
            question_objs=question_objs.filter(category__category_name__icontains=request.GET.get('category'))
        question_objs=list(question_objs)     
        data=[]
        random.shuffle((question_objs))
        for question_obj in question_objs:
            data.append({
                "category":question_obj.category.category_name,
                "question":question_obj.question,
                "marks":question_obj.marks,
                "answer":question_obj.get_answers()
            })
        payload ={'status':True,'data':data}

        return JsonResponse(payload)

    except Exception as e:
        print(e)
    return HttpResponse("Error!Something Went Wrong")        


def take_test_action(request):
    if request.method == "POST":
        deleteoption()
        category = request.POST.get('category')
        option = request.POST.get('option')
        s = Test_generation()
        s.category = category
        s.option = option
        s.save()
        return render(request,'company/category.html',{'sucess':True})
    
def delete_test(request):
    record = Test_generation.objects.all()
    record.delete()
    return render(request,'company/category.html',{'delete':True})

def score(request):
    result = test_score.objects.all()
    return render(request,'company/home1.html',{'score':result})

def score_shortlist(request):
   
    score = request.POST.get('score')
    record = test_score.objects.all().values()
    print(type(score))
    score = int(score)
    print(type(score))

    for x in record:
        s = x['score']
        print(s)
        print(type(s))
        if score <= s:
            print("hi")
            student = test_shortlist(email=x['email'],score=x['score'])
            student.save()
    shortlist = test_shortlist.objects.all().values()
    return render(request, 'company/score_shortlist.html',{'score': shortlist}) 

def finalshortlist(request):
   
    common_emails = ShortList.objects.filter(email__in=test_shortlist.objects.values('email'))
    for email in common_emails:
            final_shortlist.objects.create(email=email.email)
            
    result = final_shortlist.objects.all().values()
    # return HttpResponse(result)
    return render(request,'company/final_shortlist.html',{'final':result})