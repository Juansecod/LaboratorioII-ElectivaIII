from django.contrib import admin
from .models import User, Team, Task

admin.register(User)
admin.register(Team)
admin.register(Task)