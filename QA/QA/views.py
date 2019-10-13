from django.shortcuts import redirect


def redirect_QA(request):
    return redirect('questions_list_url', permanent=True)