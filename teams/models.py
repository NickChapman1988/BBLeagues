from django.db import models
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
