from django.shortcuts import render, redirect, get_object_or_404
from .models import Signup, Task
from datetime import datetime, date

# Login View
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Signup.objects.filter(username=username, password=password).first()

        if user:
            request.session['username'] = username
            return redirect('task_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Signup View
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            return render(request, 'signup.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        if Signup.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})

        Signup.objects.create(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'signup.html')

# Welcome View
def welcome(request):
    return render(request, 'welcome.html')

# Task List View
def task_list(request):
    username = request.session.get('username')
    user = Signup.objects.filter(username=username).first()
    if not user:
        return redirect('login')

    tasks = Task.objects.filter(user=user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    completed_today = tasks.filter(is_completed=True, completion_date__date=date.today()).count()

    completed_before_deadline = 0
    for task in tasks.filter(is_completed=True):
        if task.completion_date and task.completion_date.date() <= task.due_date:
            completed_before_deadline += 1

    context = {
        'user': user,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'tasks_undone': (total_tasks - completed_tasks),
    }

    return render(request, 'task_list.html', context)

# Add Task View (Updated for no description)
def add_task(request):
    user = Signup.objects.filter(username=request.session.get('username')).first()
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')

        # Now no description is being saved
        Task.objects.create(user=user, title=title, due_date=due_date)

        return redirect('task_list')
    return render(request, 'add_task.html')

# Complete Task View
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = True
    task.completion_date = datetime.now()
    task.save()
    return redirect('task_list')

# Undo Task View
def undo_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = False
    task.completion_date = None
    task.save()
    return redirect('task_list')

# Delete Task View
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

# Edit Task View (Updated for no description)
def edit_task(request, task_id):
    username = request.session.get('username')
    user = Signup.objects.filter(username=username).first()
    if not user:
        return redirect('login')

    task = get_object_or_404(Task, id=task_id, user=user)

    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')

        task.title = title
        task.due_date = due_date
        task.save()

        return redirect('task_list')

    return render(request, 'edit_task.html', {'task': task})
