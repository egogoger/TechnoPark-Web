from django.shortcuts import render


def questions_list(request):
    return render(request, 'QA_main/index.html', context={})

def login(request):
    return render(request, 'QA_main/login.html', context={})


def signup(request):
    return render(request, 'QA_main/signup.html', context={})


def question(request):
    return render(request, 'QA_main/question.html', context={})


def ask(request):
    return render(request, 'QA_main/ask.html', context={})
