from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def setup(request):
    return render(request, 'setup.html')

def create_match(request):
    return render(request, 'match.html')

def scoreboard(request):
    return render(request, 'match.html')

def match_score(request):
    request.POST
    return render(request, 'match.html')

def undo_score(request):
    request.POST
    return render(request, 'match.html')

def reset_set(request):
    request.POST
    return render(request, 'match.html')

def next_set(request):
    request.POST
    return render(request, 'match.html')
