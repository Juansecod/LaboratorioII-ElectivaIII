from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Observation, User, Task, Team

def generate_admin(request):
    admin_users = User.objects.filter(rol='A').values()
    if(len(admin_users) == 0):
        admin = User(
            name = "Superusuario", 
            email = "admin@mail.com",
            password = make_password("12345"),
            rol = "A",
        )
        
        admin.save()
        
        messages.success(request, f"The administrator user has been successfully created with the emai: {admin.email}")
    return redirect("login")
              
def login(request):
    """ User.objects.filter().delete() """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                data_user = {
                    "id": user.id,
                    "nombre_completo": user.name,
                    "email": user.email,
                    "rol": user.rol
                }
                request.session["user"] = data_user
                messages.success(request, "Login was succesful.")
                return redirect('home')  
            else:
                messages.error(request, "Wrong password.")
        except User.DoesNotExist:
            messages.error(request, "The email is not found in our database..")

    context = {
        'current_page': "login",
        'title': "Login"
    }
    context['not_admin'] = len(User.objects.filter(rol="A").values()) < 1
    return render(request, 'login.html', context)
        
def logout(request):
    try:
        del request.session["user"]
        messages.success(request, "You have been logged out successfully.")
        return redirect("login")      
    except:
        messages.error(request, "Ups, Something way wrong")
        return redirect("home")

def home(request):
    user = request.session.get("user", None)
    if(user is None):
        messages.warning(request, "Please log in to use this function.")
        return redirect("login")
    
    if(user['rol'] == 'A'):
        return redirect('project_leads')
    
    if(user['rol'] == 'PM'):
        return redirect('developers')
    
    if(user['rol'] == 'D'):
        return redirect('teams')
    
    context = {
        "current_page": "home",
        "title": "Home"
    }
    return render(request, 'index.html', context)

""" Admin views """

def project_leads(request):
    user = request.session.get("user", None)
    
    if(user is None or user['rol'] != "A"):
        return redirect('home')
    
    context = {
        "current_page": "project_leads",
        "title": "Project Leads",
    }
    
    context['project_leads'] = User.objects.filter(rol="PM").values()
    
    return render(request, 'project_leads/project_leads.html', context)

def create_project_lead(request):
    user = request.session.get("user", None)
    
    if(user is None or user['rol'] != "A"):
        return redirect('home')
    
    if(request.method == "POST"):
        email = request.POST['email']
        name = request.POST['name']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "The email address already exists.")
            return redirect('create_project_lead')
    
        new_user = User(
            name=name,
            email=email,
            password=make_password("12345"),           
            rol="PM"
        )
        new_user.save()
    
        messages.success(request, "The project lead has been created.")
        return redirect('project_leads')
    
    context = {
        "current_page": "project_leads",
        "title": "Create Project Lead",
    }
    return render(request, "project_leads/create_project_lead.html", context)

""" Project Manager Views """
def developers(request):
    user = request.session.get("user", None)
    
    if(user is None or user['rol'] != "PM"):
        return redirect('home')
    
    context = {
        "current_page": "developers",
        "title": "Developers",
    }
    
    context['developers'] = User.objects.filter(rol="D").values()
    
    return render(request, "developers/developers.html", context)

def create_developer(request):
    user = request.session.get("user", None)
    
    if(user is None or user['rol'] != "PM"):
        return redirect('home')
    
    if(request.method == "POST"):
        email = request.POST['email']
        name = request.POST['name']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "The email address already exists.")
            return redirect('create_developer')
    
        new_user = User(
            name=name,
            email=email,
            password=make_password("12345"),           
        )
        new_user.save()
    
        messages.success(request, "The developer has been created.")
        return redirect('developers')
    
    context = {
        "current_page": "developers",
        "title": "Create Developer"
    }
    return render(request, "developers/create_developer.html", context)

def teams(request):
    user = request.session.get("user", None)
    
    if(user is None or user['rol'] == "A"):
        return redirect('home')
    
    context = {
        "current_page": "teams",
        "title": "Teams",
    }
    
    if(user['rol'] == "PM"):
        context['teams'] = Team.objects.filter(project_manager=user['id'])
    else:
        developer = User.objects.get(pk=user['id'])
        context['teams'] = developer.teams_as_developer.all()
    
    return render(request, "teams/teams.html", context)

def create_team(request):
    user = request.session.get("user", None)
    
    if(user is None or user['rol'] != "PM"):
        return redirect('home')
    
    if(request.method == "POST"):
        project_manager = User.objects.get(id=user['id'])
        developers_ids = request.POST.getlist('developers')
        developers = User.objects.filter(id__in=developers_ids)
 
        team = Team.objects.create(project_manager=project_manager)
        team.developers.set(developers)

        messages.success(request, "The team has been created.")
        return redirect('teams')
    
    context = {
        "current_page": "teams",
        "title": "Create Team"
    }
    
    context['developers'] = User.objects.filter(rol="D").values()
    return render(request, "teams/create_team.html", context)

def team(request, id_team = None):
    user = request.session.get("user", None)
    if(user is None or user['rol'] == "A"):
        return redirect('home')
    
    team = Team.objects.get(pk=id_team)
    if(user['rol'] == "PM"):
        tasks = Task.objects.filter(team=team.id).order_by("deadline")
    elif(user['rol'] == "D"):
        tasks = Task.objects.filter(team=team.id, owner=user['id'], is_dissabled = False).order_by("deadline")
        
    context = {
        "current_page": "teams",
        "title": f"Team #{team.id}",
        "team": team,
        "developers": team.developers.all(),
        "tasks": tasks
    }
    return render(request, 'teams/team.html', context)

def task(request, id_team = None, id_task = None):
    user = request.session.get("user", None)
    if(user is None or user['rol'] == "A"):
        return redirect('home')
    
    task = Task.objects.get(pk=id_task)
    observations = Observation.objects.filter(task=task)
    context = {
        "current_page": "teams",
        "title": f"Task #{id_task}",
        "task": task,
        'id_team': id_team,
        'observations': observations
    }
    return render(request, "tasks/task.html", context)

def create_task(request, id_team):
    user = request.session.get("user", None)
    if(user is None or user['rol'] != "PM"):
        return redirect('home')
    
    team = Team.objects.get(pk=id_team)
    
    if(request.method == "POST"):
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        priority = request.POST['priority']
        owner_id = request.POST['developer']
        
        owner = User.objects.get(pk=owner_id)
        
        new_task = Task(
            title = title,
            description = description,
            deadline = deadline,
            priority = priority,
            team = team,
            owner = owner
        )
        new_task.save()
        messages.success(request, "The project lead has been created.")
        return redirect('team', id_team = team.id)
    
    developers = team.developers.all()
    
    context = {
        "current_page": "teams",
        "title": f"Create Task",
        "developers": developers,
        "team": team
    }
    return render(request, "tasks/create_task.html", context)

def change_status_task(request, id_team, id_task, status):
    user = request.session.get("user", None)
    if(user is None or user['rol'] != "D"):
        return redirect('home')
    
    task = Task.objects.get(pk = id_task)
    task.status = status
    task.save()
    
    messages.success(request, f"The task has been changed to: {status}")
    return redirect('team', id_team = id_team)

def create_comment(request, id_team = None, id_task=None):
    user = request.session.get("user", None)
    if(user is None or user['rol'] != "D"):
        return redirect('home')
    
    if(request.method == 'POST'):
        comment = request.POST['comment']
        created_by = User.objects.get(pk = user['id'])
        task = Task.objects.get(pk=id_task)
        
        observation = Observation(
            comment = comment,
            created_by = created_by,
            task = task
        )
        
        observation.save()
        
        messages.success(request, "The comment has been created.")
        return redirect('task', id_team = id_team, id_task = id_task)
    
    context = {
        "current_page": "teams",
        "title": f"Create Comment",
        'id_team': id_team, 
        'id_task': id_task,
    }
    return render(request, "comments/create_comment.html", context)

def delete_task(request, id_team, id_task):
    user = request.session.get("user", None)
    if(user is None or user['rol'] != "PM"):
        return redirect('home')
    
    task = Task.objects.get(pk = id_task)
    if(task.owner is not None):
        task.is_dissabled = True
        task.save()
        status = "dissabled"
    else:
        task.delete()
        status = "deleted"
    
    messages.success(request, f"The task has been {status}.")
    return redirect('team', id_team=id_team)

def activate_task(request, id_team, id_task):
    user = request.session.get("user", None)
    if(user is None or user['rol'] != "PM"):
        return redirect('home')
    
    task = Task.objects.get(pk = id_task)

    task.is_dissabled = False
    task.save()
    status = "enabled"

    messages.success(request, f"The task has been {status}.")
    return redirect('team', id_team=id_team)