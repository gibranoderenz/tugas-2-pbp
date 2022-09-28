from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.
@login_required(login_url="/todolist/login/")
def home(request):
    tasks = Task.objects.filter(user=request.user)

    context = {"tasks": tasks, "user": request.user}
    return render(request, "todolist/home.html", context)


def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun telah berhasil dibuat!")
            return redirect("todolist:login")

    context = {"form": form}
    return render(request, "todolist/register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/todolist")
        else:
            messages.info(request, "Username atau password salah!")

    context = {}
    return render(request, "todolist/login.html", context)


def logout_user(request):
    logout(request)
    return redirect("todolist:login")


@login_required(login_url="/todolist/login/")
def create_task(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("/todolist")

    context = {"form": form}
    return render(request, "todolist/create_task.html", context)


@login_required(login_url="/todolist/login/")
def delete_task(request, id):
    task = Task.objects.filter(pk=id, user=request.user).first()
    if task:
        task.delete()
        return redirect("/todolist")
    messages.error(request, "An error occurred while deleting the task.")
    return redirect("/todolist")


@login_required(login_url="/todolist/login/")
def toggle_task(request, id):
    task = Task.objects.filter(pk=id, user=request.user).first()
    if task:
        task.is_finished = False if task.is_finished else True
        task.save()
        return redirect("/todolist")
    messages.error(request, "An error occurred while editing the task.")
    return redirect("/todolist")
