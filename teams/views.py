from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Team, Position, MemberTeam, Player
from .forms import MemberTeamForm, AddPlayerForm


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
            team.calculate_initial_treasury(reroll_cost)
            team.calculate_team_value(reroll_cost)
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
def edit_member_team(request, team_id):
    """ Edit new member team """

    team = get_object_or_404(MemberTeam, id=team_id)
    selected_team = get_object_or_404(Team, team=team.team)
    reroll_cost = selected_team.reroll_cost
    assistant_coaches = team.assistant_coaches
    cheerleaders = team.cheerleaders
    apothecary = team.apothecary_qty
    dedicated_fans = team.dedicated_fans
    reroll_qty = team.reroll_qty

    if request.method == 'POST':
        form = MemberTeamForm(request.POST, instance=team)

        if form.is_valid():
            team_edit = form.save(commit=False)
            team_edit.team = selected_team
            team_edit.league_points = team.league_points
            team_edit.total_casualties = team.total_casualties
            team_edit.total_touchdowns = team.total_touchdowns
            team_edit.edit_recalculate_treasury(reroll_cost, reroll_qty, assistant_coaches, cheerleaders, apothecary)
            team_edit.calculate_team_value(reroll_cost)
            team_edit.save()
            messages.success(request, 'Successfully edited ' + team.team_name)            
            return redirect(reverse('team_detail', args=[team.id]))

        messages.error(
            request, 'Failed to update team. Please \
            ensure the form is valid'
        )
    else:
        form = MemberTeamForm(instance=team)
        messages.info(request, f'You are editing {team.team_name}')

    template = 'teams/edit_member_team.html'
    context = {
        'team': team,
        'faction': selected_team,
        'form': form,
    }

    return render(request, template, context)


@login_required
def delete_member_team(request, team_id):
    """ Delete member team """
    
    team = get_object_or_404(MemberTeam, id=team_id)
    players = Player.objects.filter(team_name=team_id)

    if not request.user.is_superuser or request.user.username == team.manager:
        messages.error(request, "Sorry, you don't have permission to do that")
        return redirect(reverse('home'))

    if players:
        players.delete()
    team.delete()
    messages.success(request, 'Team deleted')
    return redirect(reverse('teams'))


@login_required
def add_member_player(request, team_id):
    """ Add a new player to a member team """

    team = get_object_or_404(MemberTeam, id=team_id)
    faction = get_object_or_404(Team, team=team.team)
    reroll_cost = faction.reroll_cost
    positions = Position.objects.filter(team=faction)
    players = Player.objects.filter(team_name=team)
    
    if request.method == 'POST':
        
        form = AddPlayerForm(request.POST)

        if form.is_valid():
            if team.player_qty < 16:
                player = form.save(commit=False)
                selected_position = player.position
                position = get_object_or_404(Position, id=selected_position.id)
                player.ma = position.ma
                player.st = position.st
                player.ag = position.ag
                player.pa = position.pa
                player.av = position.av
                player.skills = position.skills
                player.current_value = position.cost
                player.team_name = team
                player.spp = 0
                player_cost = position.cost
                player.save()
                team.calculate_team_value(reroll_cost)
                team.recalculate_treasury(player_cost)

                messages.success(request, 'Successfully added player "' + player.player_name + '" to "' + team.team_name + '"')            
                return redirect(reverse('team_detail', args=[team.id]))
            
            else:
                messages.error(
                    request, 'You have already added the maximum number of players to this team!'
                )
            
        messages.error(
            request, 'Failed to add player. Please \
            ensure the form is valid'
        )
    else:
        form = AddPlayerForm()

    template = 'teams/add_member_player.html'
    context = {
        'team': team,
        'faction': faction,
        'positions': positions,
        'form': form,
        'players': players
    }

    return render(request, template, context)