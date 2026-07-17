from django.contrib import admin
from .models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'priority', 'completed', 'created_at',)
    search_fields = ('title', 'description',)
    list_filter = ('priority', 'completed', 'created_at')
    
admin.site.register(Task, TaskAdmin)