from django.contrib import admin
from .models import Position, Team

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

    ordering = ('team',)


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


admin.site.register(Position, PositionAdmin)
admin.site.register(Team, TeamAdmin)
