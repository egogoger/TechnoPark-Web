from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import *
from .utils import *

QUESTIONS_PER_PAGE = 3

def questions_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        questions = Question.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        questions = Question.objects.all()

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
