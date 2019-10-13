from django.urls import path
from .views import *

urlpatterns = [
    path('',                    questions_list, name='questions_list_url'),
    path('Que_Ayy/login/',      login,          name='login_url'),
    path('Que_Ayy/signup/',     signup,         name='signup_url'),
    path('Que_Ayy/question/',   question,       name='question_url'),
    path('Que_Ayy/ask/',        ask,            name='ask_url'),

]
