from django.shortcuts import render
from .models import Task


# Create your views here.

def index(request):
    tasks = Task.objects.all()
    tasks_count = tasks.count()
    uncompleted_tasks = tasks.filter(completed=False).count()
    
    context = {'tasks': tasks, 'tasks_count': tasks_count, 'uncompleted_tasks': uncompleted_tasks}
        
    return render(request, 'base/index.html', context)


def task(request, pk):   
    task = Task.objects.get(id=pk)

    context = {'task': task}    
    
    return render(request, 'base/task.html', context)