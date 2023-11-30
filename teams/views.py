from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team, Position, MemberTeam, Player
from .forms import MemberTeamForm


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


def team_detail(request, team_id):
    """ A view to show team details """
    # Get individual team
    team = get_object_or_404(MemberTeam, id=team_id)
    players = Player.objects.filter(team_name=team_id)

    context = {
        'team': team,
        'players': players,
    }

    return render(request, 'teams/team_detail.html', context)


@login_required
def pick_team(request):
    """ Choose faction for new member team """
    teams = Team.objects.all()

    context = {
        'teams': teams,
    }

    return render(request, 'teams/pick_team.html', context)

    
@login_required
def add_member_team(request, team):
    """ Add a new member team """
    if request.method == 'POST':
        form = MemberTeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.manager = request.user
            team.save()
            messages.success(request, 'Successfully added team')
            return redirect(reverse('pick_team'))

        messages.error(
            request, 'Failed to add team. Please \
            ensure the form is valid'
        )
    else:
        form = MemberTeamForm()

    template = 'teams/add_member_team.html'
    context = {
        'form': form,
    }

    return render(request, template, context)