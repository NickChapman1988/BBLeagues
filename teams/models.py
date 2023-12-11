from django.db import models
from django.shortcuts import get_object_or_404
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
    apothecary_qty = models.IntegerField(default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    treasury = models.IntegerField(default=1000000)
    dedicated_fans = models.IntegerField(default=1, 
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    league_points = models.IntegerField(default=0)
    total_touchdowns = models.IntegerField(default=0)
    total_casualties = models.IntegerField(default=0)


    def __str__(self):
        """ String method """
        return self.team_name

    
    def calculate_initial_treasury(self, reroll_cost):
        """ Calculate remaining treasury after initial team creation """
        initial_treasury = self.treasury
        hiring_cost = 10000
        sideline_staff = self.cheerleaders + self.assistant_coaches + (self.dedicated_fans - 1)
        initial_cost = (self.reroll_qty * reroll_cost) + (sideline_staff * hiring_cost) + (self.apothecary_qty * 50000)
        
        self.treasury = initial_treasury - initial_cost
        self.save()
        return self.treasury    

    
    def calculate_team_value(self, reroll_cost):
        """ Calculate team value """
        hiring_cost = 10000
        team = get_object_or_404(MemberTeam, id=self.id)
        player_costs = 0
        players = Player.objects.filter(team_name=team)
        for player in players:
            player_costs += player.current_value
        
        sideline_staff = self.cheerleaders + self.assistant_coaches + self.dedicated_fans
        total = (self.reroll_qty * reroll_cost) + (sideline_staff * hiring_cost) + (self.apothecary_qty * 50000) + player_costs
        self.team_value = total / 1000
        self.current_team_value = self.team_value
        self.save()
        return self.current_team_value

    
    def recalculate_treasury(self, player_cost):
        """ Recalculate treasury after player purchase """
        initial_treasury = self.treasury
        self.treasury = initial_treasury - player_cost
        # increase team player count with each player purchase
        player_count = self.player_qty
        self.player_qty = player_count + 1
        self.save()
        return self.treasury

    
    def edit_recalculate_treasury(self, reroll_cost, reroll_qty, assistant_coaches, cheerleaders, apothecary):
        """ Recalculate treasury after editing team """
        initial_treasury = self.treasury
        hiring_cost = 10000
        initial_staff = cheerleaders + assistant_coaches
        initial_rerolls = reroll_qty
        costs = 0
        if self.reroll_qty != initial_rerolls:
            new_rerolls = self.reroll_qty - initial_rerolls
            costs = new_rerolls * reroll_cost
        staff_costs = 0
        new_staff = self.cheerleaders + self.assistant_coaches
        if new_staff != initial_staff:
            staff_costs = (new_staff - initial_staff) * hiring_cost
        apoc_cost = 0
        if self.apothecary_qty != apothecary:
            apoc_cost = 50000
        
        total = costs + staff_costs + apoc_cost
        self.treasury = initial_treasury - total
        self.save()


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
        return str(self.player_name) + ", " + str(self.position)
