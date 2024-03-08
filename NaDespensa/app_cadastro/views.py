from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_, logout as logout_
from django.contrib.auth.decorators import login_required

def home(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        
    return render(request, 'home/home.html', {'username': username})


def register(request):
    if request.method == "GET":
        return render(request, 'usuarios/register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username).first()
        
        if user:
            message = "Username já utilizado"
            return render(request, 'usuarios/register.html', {'message': message})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        message = "Usuário cadastrado com sucesso"
        return render(request, 'usuarios/register.html', {'message': message})


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            login_(request, user)
            return redirect('home')
        else:
            message = "Usuário ou senha inválidos!"
            return render(request, 'home/login.html', {'message': message})
    return render(request, 'usuarios/login.html')


def logout(request):
    logout_(request)
    return redirect('home')


def produtos(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'home/produtos.html', {'username': username})


@login_required(login_url="/auth/login/")
def plataforma(request):
    if request.user.is_authenticated:
        return HttpResponse("ABU")
    return HttpResponse("Você precisa estar logado! 🤬")