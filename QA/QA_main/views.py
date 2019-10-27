from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import *
from .utils import *


def questions_list(request):
    questions = Question.objects.all()
    context = paginator(request, questions, 3)
    return render(request, 'QA_main/index.html', context=context)


def question_detail(request, slug):
    q = get_object_or_404(Question, slug__iexact=slug)
    return render(request, 'QA_main/question.html', context={'question': q})


def login(request):
    return render(request, 'QA_main/login.html', context={})


def signup(request):
    return render(request, 'QA_main/signup.html', context={})


def ask(request):
    return render(request, 'QA_main/ask.html', context={})

def tags(request):
    tags = Tag.objects.all()
    return render(request, 'QA_main/tags.html', context={'tags': tags})
