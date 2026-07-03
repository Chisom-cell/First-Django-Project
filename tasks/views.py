from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# # Create your views here.
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
    
    tasks = [
        { 'id': 1, 'text': 'Cook rice and stew', 'done': True },
        { 'id': 2, 'text': 'Wash the dishes', 'done': False },
        { 'id': 3, 'text': 'Clean the house', 'done': False },
        { 'id': 4, 'text': 'Hit the gym', 'done': False },
        { 'id': 5, 'text': 'Prepare for the meeting', 'done': False },
        { 'id': 6, 'text': 'Netflix and chill', 'done': False }
        
    ]

    context = {
        'greeting': greeting,
        'tasks': tasks
    }
    
    return render(request, 'home.html', context)

def login(request):
    return render(request, 'login.html')