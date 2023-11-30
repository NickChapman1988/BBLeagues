from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Team(models.Model):
    team = models.CharField(max_length=254)
    reroll_cost =  models.IntegerField()
    special_rules = models.TextField(null=True, blank=True)
    tier = models.IntegerField()
    apothecary = models.CharField(max_length=3)


    def __str__(self):
        """ String method """
        return str(self.team)


class Position(models.Model):
    team = models.ForeignKey('Team', null=False, blank=False, on_delete=models.CASCADE)
    position_name = models.CharField(max_length=254)
    cost = models.IntegerField()
    max_qty = models.IntegerField()
    ma = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    st = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    ag = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    pa = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    av = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(11)]
    )
    skills = models.TextField(null=True, blank=True)
    primary_skills = models.CharField(max_length=5)
    secondary_skills = models.CharField(max_length=5)
    

    def __str__(self):
        """ String method """
        return str(self.position_name)


class MemberTeam(models.Model):
    team_name = models.CharField(max_length=254)
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    team = models.ForeignKey('Team', null=False, blank=False, on_delete=models.CASCADE)
    players = models.ForeignKey('Player', null=True, blank=True, on_delete=models.SET_NULL)
    team_value = models.IntegerField(default=0)
    current_team_value = models.IntegerField(default=0)
    reroll_qty = models.IntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(8)]
    )
    player_qty = models.IntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(16)]
    )
    assistant_coaches = models.IntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    cheerleaders = models.IntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(12)]
    )
    apothecary = models.IntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    treasury = models.IntegerField(default=0)
    dedicated_fans = models.IntegerField(default=1, 
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    league_points = models.IntegerField(default=0)
    total_touchdowns = models.IntegerField(default=0)
    total_casualties = models.IntegerField(default=0)


    def __str__(self):
        """ String method """
        return self.team_name


class Player(models.Model):
    team_name = models.ForeignKey('MemberTeam', null=False, blank=False, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=254, null=True, blank=True)
    player_no = models.IntegerField(null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(16)]
    )
    position = models.ForeignKey('Position', null=False, blank=False, on_delete=models.CASCADE)
    spp = models.IntegerField(null=True, blank=True)
    ma = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    st = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    ag = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    pa = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    av = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(11)]
    )
    skills = models.TextField(null=True, blank=True) 
    current_value = models.IntegerField()
    
    

    def __str__(self):
        """ String method """
        return self.player_name + ", " + str(self.position)
