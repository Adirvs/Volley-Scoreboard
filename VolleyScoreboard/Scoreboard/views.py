from django.shortcuts import render
from .forms import MatchSettingsForm

def home(request):
    return render(request, 'home.html')

def setup(request):
    if request.method == 'POST':
        form = MatchSettingsForm(request.POST)
        if form.is_valid():
            form = MatchSettingsForm(request.POST)
            return render(request, 'setup.html', {'form': form})

def create_match(request):
    if request.method == 'POST':
        # Aqui você pode processar os dados do formulário e criar a partida
        # Por enquanto, apenas renderizamos a página do placar
        return render(request, 'match.html')
    return render(request, 'match.html')

def scoreboard(request):
    return render(request, 'match.html')

def match_score(request):
    if request.method == 'POST':
        # Process the score update logic here
        pass
    return render(request, 'match.html')

def undo_score(request):
    if request.method == 'POST':
        # Process the undo score logic here
        pass
    return render(request, 'match.html')

def reset_set(request):
    if request.method == 'POST':
        # Process the reset set logic here
        pass
    return render(request, 'match.html')

def next_set(request):
    if request.method == 'POST':
        # Process the next set logic here
        pass
    return render(request, 'match.html')
