from django.urls import path
from .views import *

urlpatterns = [
	path('', 			redirect_new),
    path('new/',        questions_list_new, name='questions_list_new_url'),
    path('top/',        questions_list_top, name='questions_list_top_url'),
    path('login/',      login,          name='login_url'),
    path('signup/',     signup,         name='signup_url'),
    path('question/<str:slug>/',
    					question_detail,name='question_detail_url'),
    path('ask/',        ask,            name='ask_url'),
    path('tags/',       tags,           name='tags_url'),
    path('tag/<str:title>/',
  						tag_detail,		name='tag_detail_url'),
]
