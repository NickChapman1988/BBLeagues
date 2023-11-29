""" Forms for the Teams app """

from django import Forms
from .models import Team, Position, MemberTeam, Player


class MemberTeamForm(form.ModelForm):
    """ A form for new Member Teams """


    class Meta:
        """ Metadata for MemberTeamForm """
        model = MemberTeam
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        """ init method for MemberTeamForm """
        super().__init__(*args, **kwargs)
        teams = Team.objects.all()
        self.fields['team'].choices = teams


