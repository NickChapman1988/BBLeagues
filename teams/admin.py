from django.contrib import admin
from .models import Position, Team, MemberTeam, Player

# Register your models here.

class PositionAdmin(admin.ModelAdmin):
    """ Admin for the Position model """
    list_display = (
        'position_name',
        'team',
        'cost',
        'max_qty',
        'ma',
        'st',
        'ag',
        'pa',
        'av',
        'skills',
        'primary_skills',
        'secondary_skills',
    )

    ordering = ('id',)


class TeamAdmin(admin.ModelAdmin):
    """ Admin for the Team model """
    list_display = (
        'team',
        'reroll_cost',
        'special_rules',
        'tier',
        'apothecary',
    )

    ordering = ('team',)


class MemberTeamAdmin(admin.ModelAdmin):
    """ Admin for the MemberTeam model """
    list_display = (
        'manager',
        'team_name',
        'team',
    )

    ordering = ('manager',)


class PlayerAdmin(admin.ModelAdmin):
    """ Admin for the Player model """
    list_display = (
        'player_name',
        'team_name',
        'position',
        'ma',
        'st',
        'ag',
        'pa',
        'av',
        'skills',
        'spp',
    )

    ordering = ('team_name',)


admin.site.register(Position, PositionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(MemberTeam, MemberTeamAdmin)
admin.site.register(Player, PlayerAdmin)
