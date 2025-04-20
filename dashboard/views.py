from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomLoginForm
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Project
from .models import Task
from django.contrib.auth import logout
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)  # ✅ use your custom form
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ✅ Optional: Handle "remember me"
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Session expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm(request)
    return render(request, 'dashboard/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'dashboard/signup.html', {'form': form})

def project_list(request):
    projects = Project.objects.all()  # Get all projects from the database
    return render(request, 'dashboard/project_list.html', {'projects': projects})

from django.shortcuts import render
from .models import Task

def task_list(request):
    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')

    tasks = Task.objects.all()

    if category_filter:
        tasks = tasks.filter(category=category_filter)

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(request, 'dashboard/task_list.html', {
        'tasks': tasks,
        'category_filter': category_filter,
        'status_filter': status_filter,
    })


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'dashboard/profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(project__owner=request.user)
    stats = tasks.values('status').annotate(total=Count('id'))
    total_tasks = tasks.count()
    projects = Project.objects.filter(owner=request.user)

    # Add progress report logic
    project_data = []
    for project in projects:
        project_tasks = tasks.filter(project=project)
        total_tasks_project = project_tasks.count()
        completed_tasks = project_tasks.filter(status='complete').count()

        completion_percentage = (completed_tasks / total_tasks_project) * 100 if total_tasks_project > 0 else 0

        project_data.append({
            'project': project,
            'completion_percentage': completion_percentage,
            'total_tasks': total_tasks_project,
            'completed_tasks': completed_tasks,
            'task_status_summary': project_tasks.values('status').annotate(total=Count('id'))
        })

    return render(request, 'dashboard/dashboard.html', {
        'tasks': tasks,
        'stats': stats,
        'total_tasks': total_tasks,
        'projects': projects,
        'project_data': project_data  # Pass it to the template
    })

    
from django.contrib.auth.decorators import login_required


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user  # Assign the logged-in user as the owner
            project.save()
            from django.contrib import messages
            messages.success(request, "Project created successfully.") 
            return redirect('project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'dashboard/project_form.html', {'form': form, 'edit': False})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)  # Bind the form with existing project data
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, "Project updated successfully.")
            # Save the updated project
            return redirect('project_list')  # Redirect to the project list after editing
    else:
        form = ProjectForm(instance=project)  # Pre-fill the form with the project's current data

    return render(request, 'dashboard/project_form.html', {'form': form, 'edit': True})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('dashboard')
    return render(request, 'dashboard/project_confirm_delete.html', {'project': project})

from django.shortcuts import get_object_or_404

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        category = request.POST.get('category')
        status = request.POST.get('status')
        project_id = request.POST.get('project')
        project = Project.objects.get(id=project_id, owner=request.user)

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            category=category,
            status=status,
            project=project
        )
        return redirect('dashboard')

    projects = Project.objects.filter(owner=request.user)
    return render(request, 'dashboard/task_create.html', {'projects': projects})


from django.shortcuts import get_object_or_404
from .models import Task
from .forms import TaskForm  # Make sure you have a TaskForm

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or wherever your task list is
    else:
        form = TaskForm(instance=task)
    return render(request, 'dashboard/edit_task.html', {'form': form, 'task': task})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('dashboard')  # or task list
    return render(request, 'dashboard/delete_task.html', {'task': task})


def logout_view(request):
    logout(request)
    return redirect('login') 


from django.shortcuts import render
from django.db.models import Count
from .models import Task, Project

def progress_report_view(request):
    tasks = Task.objects.filter(project__owner=request.user)

    # Apply filters if provided
    project_id = request.GET.get('project')
    category_filter = request.GET.get('category')

    if project_id:
        tasks = tasks.filter(project__id=project_id)

    if category_filter:
        tasks = tasks.filter(category=category_filter)

    projects = Project.objects.filter(owner=request.user)

    # Initialize a list to hold task completion data per project
    project_data = []

    for project in projects:
        project_tasks = tasks.filter(project=project)
        
        total_tasks = project_tasks.count()
        completed_tasks = project_tasks.filter(status='complete').count()
        
        if total_tasks > 0:
            completion_percentage = (completed_tasks / total_tasks) * 100
        else:
            completion_percentage = 0
        
        project_data.append({
            'project': project,
            'completion_percentage': completion_percentage,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'task_status_summary': project_tasks.values('status').annotate(total=Count('id'))
        })

    # Return the data to the template
    return render(request, 'dashboard/progress_report.html', {
        'project_data': project_data,
        'projects': projects,
        'project_id': project_id,
        'category_filter': category_filter
    })






