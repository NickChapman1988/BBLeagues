""" Forms for the Teams app """

from django import forms
from .models import Team, Position, MemberTeam, Player


class MemberTeamForm(forms.ModelForm):
    """ A form for new Member Teams """

    class Meta:
        """ Metadata for MemberTeamForm """
        model = MemberTeam
        fields = [
            "team_name",  
            "reroll_qty", 
            "assistant_coaches", 
            "cheerleaders", 
            "apothecary_qty", 
            "dedicated_fans",
        ]
    
    def __init__(self, *args, **kwargs):
        """ init method for MemberTeamForm """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class AddPlayerForm(forms.ModelForm):
    """ A form for adding new players to a member team """

    class Meta:
        """ Metadata for AddPlayerForm """
        model = Player
        fields = [
            "player_name",
            "player_no",
            "position",
        ]
    
    def __init__(self, *args, **kwargs):
        """ init method for AddPlayerForm """
        super().__init__(*args, **kwargs)
        member_team = get_object_or_404(MemberTeam, id=team_id)
        positions = Position.objects.filter(team=member_team)
        players = [(p.id, p.position_name) for p in positions]

        self.fields['position'].choices = players
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
            