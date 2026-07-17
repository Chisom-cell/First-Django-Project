from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Consolidated imports
from .models import Task
from .forms import TaskForm, Registerform 

# Helper function to generate greetings (DRF/Clean code practice)
def get_greeting():
    date = datetime.now()
    h = int(date.strftime('%H'))
    if h < 12:
        return 'Good morning! Stells'
    elif h < 16:
        return 'Good afternoon! Stells'
    elif h < 18:
        return 'Good evening! Stells'
    else:
        return 'Good night! Stells'


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already Signed In!')
        return redirect('home')
    
    form = Registerform()
    errors = None
    
    if request.method == "POST":
        form = Registerform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Account Created and Login Successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('login')
        else:
            errors = form.errors.as_data()
            messages.error(request, str(errors))
            return redirect('register')
        
    context = {
        'form': form,
        'errors': errors
    }
    return render(request, 'tasks/register.html', context)
    

@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    progress = 0
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)

    context = {
        'greeting': get_greeting(),
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress': progress,
    }

    return render(request, 'tasks/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already Logged In!')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password!')
            return redirect("login")
    return render(request, 'tasks/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_task(request):
    forms = TaskForm()
    if request.method == 'POST':
        forms = TaskForm(request.POST)
        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('home')
        else:
            return redirect('add_task')

    context = {
        'forms': forms
    }
    return render(request, "tasks/add_task.html", context)


@login_required(login_url='login')
def filter_tasks(request, foo):
    # FIXED: Changed '==' to '=' below
    if foo == "true":
        tasks = Task.objects.filter(done=True, user=request.user).order_by('-created_at')
    elif foo == 'false':
        tasks = Task.objects.filter(done=False, user=request.user).order_by('-updated_at')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'greeting': get_greeting(),  # Added so greeting doesn't break on filter pages
        'tasks': tasks
    }
    return render(request, 'tasks/home.html', context)


@login_required(login_url='login')
def update_task(request, pk):
    # FIXED: Removed the duplicate unsafe Task.objects.get line
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():  # FIXED: Removed space between form and .is_valid()
            form.save()
            messages.success(request, 'Successfully Updated!')
            return redirect('home')
        else:
            return redirect('update_task', pk=pk) # FIXED: Pointed back to update redirect name
        
    context = {
        'task': task,
        'form': form
    }
    return render(request, 'tasks/update_task.html', context)


@login_required(login_url='login')
def delete_task(request, pk):
    # FIXED: Secure restriction added so users can only delete their own tasks
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return redirect('home')  # FIXED: Passed string route name instead of function reference


@login_required(login_url='login')
def complete_task(request, pk):
    task = get_object_or_404(
        Task,
        id=pk,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect('home')