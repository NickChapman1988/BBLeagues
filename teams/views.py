from django.shortcuts import render, get_object_or_404
from .models import Team, Position, MemberTeam, Player

# Create your views here.


def teams(request):
    """ A view to display the teams page, including user's teams """
    teams = None

    if request.user.is_authenticated:
        teams = MemberTeam.objects.filter(manager=request.user)
    
    context = {
        'teams' : teams,
    }
    
    return render(request, 'teams/teams.html', context)