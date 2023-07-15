from django.contrib import admin
from django.urls import path
from student import views
from .views import *

urlpatterns = [
    path('',company_register), 
    path('company_register/',company_register),
    path('login/',login_company),
    path('home/',home),
    path('sort/',sorting),
    path('test/',test_generate),
    # path('get_quiz/',get_quiz),
    path('deleteshortlist/',deleteshortlist),
    # path('quiz/',quiz),
    path('take_test_action/',take_test_action),
    path('delete_test/',delete_test),
    path('score/',score),
    path('score_shortlist/',score_shortlist),
    path('final_shortlist/',finalshortlist),
    # path('calculate_score/',calculate_score),
] 