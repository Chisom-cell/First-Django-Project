from django.urls import path
from tasks.views import home, login

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
]