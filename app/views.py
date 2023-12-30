from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Task
from app.forms import TaskForm



def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or dashboard
            return redirect('home' , current_tab='all')  # Replace 'dashboard' with the actual URL name
        else:
            # Handle invalid login credentials (e.g., show an error message)
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

def RegisterPage(request):
    if request.method == 'POST':
        # Get the form data from the request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Username or email already exists'})

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Log the user in
        login(request, user)

        # Redirect to a success page or dashboard
        return redirect('home' ,current_tab='all')  # Replace 'home' with the actual URL name

    return render(request, 'register.html')

def LogoutPage(request) :
    logout(request)
    return redirect(reverse('login'))


@login_required
def HomePage(request, current_tab):
    tasks =[]
    if current_tab == 'active':
        tasks = Task.objects.filter(user=request.user,is_completed=False)
    elif current_tab == 'completed':
        tasks = Task.objects.filter(user=request.user,is_completed=True)
    elif current_tab == 'all':
        tasks = Task.objects.filter(user=request.user)

    form = TaskForm()
    tasks = reversed(list(tasks))

    return render(request, 'index.html', {'tasks': tasks, 'current_tab': current_tab, 'form' : form})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task = Task(user=request.user, task_name=task_name)
            task.save()
            return redirect('home', current_tab='all')

    return redirect('home', current_tab='all')


def complete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    
    # Ensure the task belongs to the currently logged-in user before marking it as completed
    if task.user == request.user:
        if task.is_completed :
            task.is_completed = False
            task.save()
        else :
            task.is_completed = True
            task.save()
    return redirect('home' , current_tab='all')

def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    
    # Ensure the task belongs to the currently logged-in user before deleting it
    if task.user == request.user:
        task.delete()
    return redirect('home' , current_tab='all')