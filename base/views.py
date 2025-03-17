from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import UserForm, TaskForm


# Create your views here.

def registerPage(request):

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
    
    else:
        form = UserForm()
    
    context = {'form': form}
    
    return render(request, 'base/register.html', context)


def loginPage(request):
    # Um usuário já autenticado não consegue acessar essa página:
    if request.user.is_authenticated:
        return redirect('index')
    
    # Se a requisição é POST, precisamos processar os dados do formulário:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verificando se o usuário existe:
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')
            
        # Autenticando o usuário:
        user = authenticate(username=username, password=password)
        
        # Se as credenciais são válidas:
        if user is not None:
            login(request, user) # loga o usuário
            
            return redirect('index')
        
        else:
            messages.error(request, "Invalid Username OR Password!")
        
    return render(request, 'base/login.html')
    

def logoutPage(request):
    logout(request)
    
    return redirect('login')

    
@login_required(login_url='login')
def index(request):
    # Se a requisição é POST, precisamos processar os dados do formulário:
    if request.method == 'POST':
        task_title = request.POST.get('new-task')
        
        if task_title != '':
            task = Task.objects.create(
                user=request.user,
                title=task_title,
            )
    
    # Obtém todas as tasks do usuário:
    tasks = Task.objects.filter(user=request.user)
    tasks_count = tasks.count()
    uncompleted_tasks = tasks.filter(completed=False).count()
        
    context = {'tasks': tasks, 'tasks_count': tasks_count, 'uncompleted_tasks': uncompleted_tasks}
        
    return render(request, 'base/index.html', context)


@login_required(login_url='login')
def task(request, pk):   
    task = Task.objects.get(id=pk)

    context = {'task': task}    
    
    return render(request, 'base/task.html', context)


@login_required(login_url='login')
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    
    # Se a requisição é POST, precisamos processar os dados do formulário:
    if request.method == 'POST':
        form = TaskForm(request.POST)
        
        # Verifica se o formulário é válido:
        if form.is_valid():
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            
            # Só atualiza completed se a opção for selecionada:
            if request.POST.get('completed') is not None:
                task.completed = request.POST.get('completed')
            
            task.save() # atualiza os dados da task
            
            return redirect('index')
            
    context = {'form': form}
    
    return render(request, 'base/update_task.html', context)
