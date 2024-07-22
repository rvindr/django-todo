from django.shortcuts import render, redirect
from .models import Todo
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_desc = request.POST.get('task_desc')
        task_img = request.FILES.get('task_img')

        # saving data to model
        Todo.objects.create(name=task_name, desc=task_desc, img=task_img)
        
        
        return redirect('index')

    if request.GET.get('search'):
        queryset = Todo.objects.filter(name__icontains=request.GET.get('search'))
        context = {
            'todo':queryset
        }
        return render(request,'core/index.html', context)



    context = {
            'todo' : Todo.objects.all()
        }
    return render(request,'core/index.html', context)



def delete_task(request, id):

    query = Todo.objects.get(id=id)
    query.delete()


    return redirect('index')

def update_task(request, id):

    if request.method == "POST":
        task_name = request.POST.get('task_name')
        task_desc = request.POST.get('task_desc')
        task_img = request.FILES.get('task_img')

        query = Todo.objects.get(id=id)
        query.name = task_name
        query.desc = task_desc
        if task_img:
            query.img = task_img

        query.save()

        return redirect('index')

    context = {
        'todo':Todo.objects.get(id=id)
    }
    return render(request,'core/update.html',context)




def register(request):

    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect('/register/')
        
        user = User.objects.create(first_name = first_name,
                last_name = last_name,
                email = email,
                username = username
                )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully!.")
        return redirect('login')

    return render(request,'core/register.html')

def login_page(request):

    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, "Invalid username.")
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid password!.")
            return redirect('login')
        else:
            login(request, user)
            return redirect('index')

    return render(request, 'core/login.html')
def logout_page(request):
    logout(request)
    return redirect('login')