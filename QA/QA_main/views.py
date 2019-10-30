from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q

from .models import *
from .utils import *

QUESTIONS_PER_PAGE = 3


def redirect_new(request):
    return redirect('questions_list_new_url', permanent=True)
    

def questions_list_new(request):
    questions = Question.objects.show_new()

    context = paginator(request, questions, QUESTIONS_PER_PAGE)
    return render(request, 'QA_main/index.html', context=context)


def questions_list_top(request):
    search_query = request.GET.get('search', '')

    if search_query:
        questions = Question.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        questions = Question.objects.show_top()

    context = paginator(request, questions, QUESTIONS_PER_PAGE)
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


def tag_detail(request, title):
    t = Tag.objects.get(title__iexact=title)

    questions = t.questions.all()
    context = paginator(request, questions, QUESTIONS_PER_PAGE)

    context['tag'] = t
    return render(request, 'QA_main/tag_detail.html', context)
