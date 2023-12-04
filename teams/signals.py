"""
Teams app signal config module
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import MemberTeam


@receiver(post_save, sender=MemberTeam)
def update_treasury_and_tv_on_add(sender, instance, **kwargs):
    """ Update team treasury and team value when created """
    instance.calculate_treasury_and_tv()
