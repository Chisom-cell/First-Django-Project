from django.urls import path
from tasks.views import home, login, add_task, filter_tasks, update_task, delete_task

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('add_task/', add_task, name='add_task'),
    path('tasks/<str:foo>/', filter_tasks, name='tasks'),
    path('task/<int:pk>/', update_task, name='task'),
    path('task/<int:pk>', delete_task, name='delete')
]