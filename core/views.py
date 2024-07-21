from django.shortcuts import render, redirect
from .models import Todo

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

def login(request):
    return render(request,'core/login.html')
def register(request):
    return render(request,'core/register.html')