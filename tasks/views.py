from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .forms import TaskForm, Registerform 
from .models import Task


# # Create your views here.
def register_view(request):
    if request.user.is_authenticated:
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
                return redirect('home')
            else:
                return redirect('login')
        else:
            errors = form.errors.as_data()
            return redirect('register')
        
    context = {
        'form': form,
        'errors': errors
    }
    return render(request, 'register.html', context)
    

# def home(request):   # request is compulsory for any view functionnyou are creating
#     return HttpResponse('<h1>Welcome to codesignature\'s website<h1>')

def home(request):
    date = datetime.now()
    h = int(date.strftime('%H'))
    
    msg = 'Good '
    
    if h < 12:
        msg  += 'morning'
    elif h < 16:
        msg += 'afternoon'
    elif h < 18:
        msg += 'evening'
    else:
        msg += 'night'
        
    greeting = f'{msg}! Stells'
    tasks =Task.objects.all().order_by('-created_at')
    # tasks = Task.objects.all()  # Fetch all tasks from the database
    
    # tasks = [
    #     { 'id': 1, 'text': 'Cook rice and stew', 'done': True },
    #     { 'id': 2, 'text': 'Wash the dishes', 'done': False },
    #     { 'id': 3, 'text': 'Clean the house', 'done': False },
    #     { 'id': 4, 'text': 'Hit the gym', 'done': False },
    #     { 'id': 5, 'text': 'Prepare for the meeting', 'done': False },
    #     { 'id': 6, 'text': 'Netflix and chill', 'done': False }
        
    # ]

    context = {
        'greeting': greeting,
        'tasks': tasks
    }
    
    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect("login")
    return render(request, 'login.html')

def logout_view(request):
    user = request.user
    logout(request)
    return redirect('login')

def add_task(request):
    forms = TaskForm()
    if request.method == 'POST':
        forms = TaskForm(request.POST)
        
        # ========================= 
        # check for form validation
        # ==========================
        if forms.is_valid():
            forms.save()
        
            return redirect('home')

        else:
            return redirect('add_task')

    context = {
        'forms': forms
    }
    
    return render(request, "add_tasks.html", context)

def filter_tasks(request, foo):
    if foo == "true":
        tasks = Task.objects.filter(done=True).order_by('-created_at')
    elif foo == 'false':
        tasks == Task.objects.filter(done=False).order_by('-updated_at')
    else:
        tasks =Task.objects.all().order_by('-created_at')
    
    context = {
        'tasks': tasks
    }
    return render(request,'home.html', context)

def update_task(request, pk):
    task = Task.objects.get(id=pk)
    task = get_object_or_404(Task, id=pk)
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        
        if form .is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('task', pk=pk)
        
    context = {
        'task': task,
        'form': form
    }
    
    return render(request, 'update_task.html', context)

def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    
    task.delete()
    return redirect(home)
