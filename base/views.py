from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages

from .models import Task
from .forms import UserForm


# Create your views here.

def registerPage(request):
    form = UserForm()
    
    # Se a requisição é POST, precisamos processar os dados do formulário:
    if request.method == 'POST':
        # Cria a instância do formulário com os dados já preenchidos:
        form = UserForm(request.POST)
        
        # Verifica se o formulário é válido:
        if form.is_valid():
            user = form.save(commit=False) # ainda não salva no banco de dados
            user.username = user.username.lower()
            user.save()
            
            return redirect('index')
    
        else:
            messages.error(request, "An error occurred during registration!")
    
    context = {'form': form}
    return render(request, 'base/register.html', context)


def loginPage(request):
    pass
    

def logoutPage(request):
    pass
    

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
