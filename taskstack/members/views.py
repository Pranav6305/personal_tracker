from django.shortcuts import render, redirect, get_object_or_404
from .models import Signup, Task
from datetime import datetime, date

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

def welcome(request):
    return render(request, 'welcome.html')

from datetime import date
from django.shortcuts import render, redirect
from .models import Signup, Task

def task_list(request):
    # Get the logged-in user
    username = request.session.get('username')
    user = Signup.objects.filter(username=username).first()
    if not user:
        return redirect('login')

    # Get only the tasks of that user
    tasks = Task.objects.filter(user=user)

    # Calculate the counts
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    completed_today = tasks.filter(is_completed=True, completion_date__date=date.today()).count()

    # Manually check for completed before deadline
    completed_before_deadline = 0
    for task in tasks.filter(is_completed=True):
        if task.completion_date and task.completion_date.date() <= task.due_date:
            completed_before_deadline += 1

    context = {
        'user': user,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'tasks_undone':(total_tasks-completed_tasks),
    }

    return render(request, 'task_list.html', context)

def add_task(request):
    user = Signup.objects.filter(username=request.session.get('username')).first()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Task.objects.create(user=user, title=title, description=description, due_date=due_date)
        return redirect('task_list')
    return render(request, 'add_task.html')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = True
    task.completion_date = datetime.now()
    task.save()
    return redirect('task_list')

def undo_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = False
    task.completion_date = None
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')
