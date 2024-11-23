from django.db import models

class User(models.Model):
    name = models.CharField(max_length=150, null=False, default="Anonymous")
    email = models.EmailField(null = False, blank = False, unique=True)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    ROLES = (
        ("A", "Admin"),
        ("PM", "Project Manager"),
        ("D", "Developer")
    )
    rol = models.CharField(max_length = 2, choices = ROLES, default = "D")
    
class Team(models.Model):
    project_manager = models.ForeignKey(User, on_delete = models.PROTECT,  related_name='teams_as_manager')
    developers = models.ManyToManyField(User,  related_name='teams_as_developer')

class Task(models.Model):
    title = models.CharField(max_length = 255, null = False, blank = False)
    description =  models.TextField()
    deadline = models.DateField()
    start_date = models.DateTimeField(auto_now=True)
    is_dissabled = models.BooleanField(default = False)
    status = models.CharField(max_length=10, default = "To Do")
    team = models.ForeignKey(Team, on_delete = models.PROTECT)
    owner = models.ForeignKey(User, on_delete = models.PROTECT, null=True, blank=True)
    
    TYPES_PRIORITY = (
        ("L", "Lower"),
        ("M", "Medium"),
        ("H", "Higher")
    )
    priority = models.CharField(max_length = 1, choices = TYPES_PRIORITY, default = "M")
    
class Observation(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.TextField(null=True)