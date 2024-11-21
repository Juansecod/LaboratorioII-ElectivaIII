from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("login", views.login, name = "login"),
    path("logout", views.logout, name = "logout"),
    path("generate_admin", views.generate_admin, name = "generate_admin"),
    
    # Admin paths
    path("project_leads", views.project_leads, name = "project_leads"),
    path("project_leads/create", views.create_project_lead, name = "create_project_lead"),
    
    # Project Manager paths
    path("developers", views.developers, name = "developers"),
    path("developers/create", views.create_developer, name = "create_developer"),
    path("teams", views.teams, name = "teams"),
    path("teams/create", views.create_team, name = "create_team"),
    path("teams/<int:id_team>", views.team, name = "team"),
    path("teams/<int:id_team>/tasks/create", views.create_task, name="create_task"),
    path("teams/<int:id_team>/tasks/<int:id_task>", views.task, name="task"),
    path("teams/<int:id_team>/tasks/<int:id_task>/delete", views.delete_task, name="delete_task"),
    path("teams/<int:id_team>/tasks/<int:id_task>/activate", views.activate_task, name="activate_task"),
    path("teams/<int:id_team>/tasks/<int:id_task>/<str:status>", views.change_status_task, name="change_status_task"),
    path("teams/<int:id_team>/tasks/<int:id_task>/comments/create", views.create_comment, name="create_comment"),
]