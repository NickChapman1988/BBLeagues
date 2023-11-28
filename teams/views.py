from django.shortcuts import render, get_object_or_404
from .models import Team, Position

# Create your views here.


def teams(request):
    """ A view to return the index page """

    teams = Team.objects.all()
    

    context = {
        'teams' : teams,
    }
    
    return render(request, 'teams/teams.html', context)