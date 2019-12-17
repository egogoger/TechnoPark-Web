from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from .utils import *
from .forms import *


def redirect_new(request):
    return redirect('questions_list_new_url', permanent=True)
    

def questions_list_new(request):
    questions = Question.objects.show_new()

    context = paginator(request, questions)
    context['mode'] = 'new'
    return render(request, 'QA_main/index.html', context=context)


def questions_list_top(request):
    search_query = request.GET.get('search', '')

    if search_query:
        questions = Question.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        questions = Question.objects.show_top()

    context = paginator(request, questions)
    context['mode'] = 'top'
    return render(request, 'QA_main/index.html', context=context)


def users_questions(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    questions = Question.objects.show_users(profile)

    context = paginator(request, questions)
    context['profile'] = profile
    return render(request, 'QA_main/users_questions.html', context=context)


def question_detail(request, id):
    q = get_object_or_404(Question, id=id)

    context = paginator(request, q.answers.all())
    context['question'] = q
    return render(request, 'QA_main/question.html', context=context)


def log_in(request):
    if request.user.is_authenticated:
        print("is_authenticated")
        #This one shouldn't even be able to be triggered
        return redirect('success_signup_url')
    if request.method == 'POST':
        print("POST")
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            print("here")
            user = authenticate(request,
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                print(user)
                login(request, user)
                return redirect('questions_list_new_url')
            else:
                raise forms.ValidationError("User not found")
    else:
        print("GET")
        form = LoginForm()
    return render(request, 'QA_main/login.html', context={'form': form})


@login_required(redirect_field_name='login_url')
def log_out(request):
    logout(request)
    return redirect('questions_list_new_url')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            Profile.objects.save(form.cleaned_data, request.FILES['avatar'])
            user = User.objects.get(username=form.cleaned_data['username'])
            login(request, user)
            return redirect('success_signup_url')
    else:
        form = SignUpForm()
    return render(request, 'QA_main/signup.html', context={'form': form})


@login_required(redirect_field_name='login_url')
def success_signup(request):
    return render(request, 'QA_main/success_signup.html', context={})


@login_required(redirect_field_name='login_url')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        current_user = Profile.objects.get(user=request.user)

        if form.is_valid():
            send_message(form.cleaned_data)
            Question.objects.save(form.cleaned_data, current_user)
            return redirect('question_detail_url', id=(Question.objects.get(title__iexact=form.cleaned_data['title'],
                                                                            body__iexact=form.cleaned_data['body']).pk))
    else:
        form = QuestionForm()
    return render(request, 'QA_main/ask.html', context={'form': form})


def tags(request):
    tags = Tag.objects.all()
    return render(request, 'QA_main/tags.html', context={'tags': tags})


def tag_detail(request, title):
    t = Tag.objects.get(title__iexact=title)

    questions = t.questions.all()
    context = paginator(request, questions)

    context['tag'] = t
    return render(request, 'QA_main/tag_detail.html', context)



# pip install requests
from django.conf import settings
import json
import requests
def send_message(question):
    command = {
        "method": "publish",
        "params": {
            "channel": "new_posts",
            "data": {
                "question_title": "blablabla",
            }
        }
    }

    headers = {
        "Content-type": "application/json",
        "Authorization": "apikey " + settings.CENTRIFUGO_KEY
    }

    print("send message post")
    
    requests.post(
        "http://{}/api".format(settings.CENTRIFUGO_HOST),
        data=json.dumps(command),
        headers=headers,
    )





