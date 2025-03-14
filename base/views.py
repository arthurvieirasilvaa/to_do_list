from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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