from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_, logout as logout_
from django.contrib.auth.decorators import login_required
from .models import Produto
from .forms import ProdutoForm

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
        render(request, 'usuarios/register.html', {'message': message})
        return redirect('login')


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


@login_required(login_url="/auth/login/")
def produtos(request):
    username = request.user.username
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.usuario = request.user
            produto.save()
            return redirect('produtos')
    else:
        form = ProdutoForm()

    produtos = Produto.objects.filter(usuario=request.user)
    
    # Excluir produtos com quantidade igual a 0
    for produto in produtos:
        if produto.quantidade == 0:
            produto.delete()
    return render(request, 'home/produtos.html', {'form': form, 'produtos': produtos, 'username': username},)

@login_required
def aumentar_quantidade(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user)
    if produto.quantidade > 0:
        produto.quantidade += 1
        produto.save()
    return redirect('produtos')

@login_required
def diminuir_quantidade(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user)
    if produto.quantidade > 0:
        produto.quantidade -= 1
        produto.save()
    return redirect('produtos')

@login_required
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == 'POST':
        produto.delete()
        return redirect('produtos')
    return redirect('produtos')


def sobre(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        
    return render(request, 'home/sobre.html', {'username': username})


def contato(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        
    return render(request, 'home/contato.html', {'username': username})


@login_required(login_url="/auth/login/")
def plataforma(request):
    if request.user.is_authenticated:
        return HttpResponse("ABU")
    return HttpResponse("Você precisa estar logado! 🤬")