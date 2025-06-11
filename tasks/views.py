from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):
	if request.method == "GET":	
		return render(request,"signup.html",{
			"form":UserCreationForm
		})

	if request.method == "POST":
		if request.POST["password1"] == request.POST["password2"]:
			#register users
			try:
				user = User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
				user.save()
				login(request,user)
				return redirect("tasks")
			except IntegrityError:
				return render(request,"signup.html",{
			"form":UserCreationForm,
			"error":"El usuario ya existe"
		})

		return render(request,"signup.html",{
			"form":UserCreationForm,
			"error":"Confirma tu contraseña correctamente"
		})

def home(request):
	return render(request, "home.html")

@login_required
def tasks(request):
		tasks = Task.objects.filter(user=request.user)[::-1]
		return render(request,"tasks.html",{"tasks":tasks
			})


def signout(request):
	logout(request)
	return redirect("home")

def signin(request):
	if request.method == "GET":
		return render(request,"signin.html",{
			'form':AuthenticationForm
		})
	if request.method == "POST":
		user = authenticate(request, username = request.POST["username"],password = request.POST["password"])
		if user is None:
			return render(request,"signin.html",{
			'form':AuthenticationForm,
			'error':"Usuario o contraseña incorrectas"
		})
		else:
			login(request, user)
			return redirect('tasks')


@login_required
def create_tasks(request):
	if request.method == "GET":
		return render(request,"create_tasks.html",{
			"form":TaskForm
			})
	if request.method == "POST":
		try:
			form = TaskForm(request.POST)
			new_task = form.save(commit = False)
			new_task.user = request.user
			new_task.save()
			return redirect("tasks")
		except ValueError:
			return render(request,"create_tasks.html",{
			"form":TaskForm,
			"error":"Ingresa Los Datos Correctamente"
			})

@login_required
def task_detail(request, id):
	if request.method == "GET":
		task = get_object_or_404(Task,pk=id)
		form = TaskForm(instance = task)
		return render(request, "task_detail.html",{
			"task":task,
			"form":form
			})
	else:
		try:
			task = get_object_or_404(Task, pk = id, user = request.user)
			form = TaskForm(request.POST, instance = task)
			form.save()
			return redirect('tasks')
		except ValueError:
			task = get_object_or_404(Task,pk=id, user = request.user)
			form = TaskForm(instance = task)
			return render(request, "task_detail.html",{
				"task":task,
				"form":form,
				"error":"Lo siento no colocaste bien los datos"
				})


@login_required
def complete_task(request, id):
	if request.method == "POST":

		task = get_object_or_404(Task, pk = id, user = request.user)
		task.datecompleted = timezone.now()
		task.save()
		return redirect("tasks")

@login_required
def delete_task(request, id):
	if request.method == "POST":
		task = get_object_or_404(Task, pk = id, user = request.user)
		task.delete()
		return redirect("tasks")