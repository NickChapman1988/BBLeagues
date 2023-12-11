from django.urls import path
from . import views

urlpatterns = [
    path('', views.teams, name='teams'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('pick_team/', views.pick_team, name='pick_team'),
    path('add_member_team/<int:team_id>', views.add_member_team, name='add_member_team'),
    path('edit_member_team/<int:team_id>', views.edit_member_team, name='edit_member_team'),
    path('add_member_player/<int:team_id>', views.add_member_player, name='add_member_player'), 
]
