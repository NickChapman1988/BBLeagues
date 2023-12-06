from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
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
def add_member_team(request, team_id):
    """ Add a new member team """
    selected_team = get_object_or_404(Team, id=team_id)
    reroll_cost = selected_team.reroll_cost

    if request.method == 'POST':
        form = MemberTeamForm(request.POST)

        if form.is_valid():
            team = form.save(commit=False)
            team.manager = request.user
            team.team = selected_team
            team.calculate_treasury_and_tv(reroll_cost)
            team.save()
            messages.success(request, 'Successfully added team')            
            return redirect(reverse('teams'))

        messages.error(
            request, 'Failed to add team. Please \
            ensure the form is valid'
        )
    else:
        form = MemberTeamForm()

    template = 'teams/add_member_team.html'
    context = {
        'team': selected_team,
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_member_player(request, team_id):
    """ Add a new player to a member team """

    team = get_object_or_404(MemberTeam, id=team_id)
    faction = get_object_or_404(Team, id=team.team)
    positions = Position.objects.filter(id=faction)
    
    if request.method == 'POST':
        form = AddPlayerForm(request.POST)

        if form.is_valid():
            player = form.save(commit=False)
            selected_position = player.position
            position = get_object_or_404(Position, id=selected_position)
            player.ma = position.ma
            player.st = position.st
            player.ag = position.ag
            player.pa = position.pa
            player.av = position.av
            player.skills = position.skills
            player.current_value = position.cost
            player.team_name = team.team_name
            player.spp = 0
            player.save()
            messages.success(request, 'Successfully added' + player.player_name + 'to' + player.team_name)            
            return redirect(reverse('team_detail', args=[team.id]))
            
        messages.error(
            request, 'Failed to add player. Please \
            ensure the form is valid'
        )
    else:
        form = AddPlayerFormForm()

    template = 'teams/add_member_player.html'
    context = {
        'team': team,
        'faction': faction,
        'positions': positions,
        'form': form,
    }

    return render(request, template, context)