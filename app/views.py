from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request):
        pass


def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")

    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        user = User.objects.filter(username=username).first()
        if user:
            return HttpResponse("Já existe um usuário com esse username")
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return HttpResponseRedirect(reverse("login"))


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        senha = request.POST.get("senha")
    user = authenticate(username=username, password=senha)
    if user:
        login_django(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponse("Usuário ou senha inválidos")


def logout(request):
    logout_django(request)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/auth/login/")
def home(request):
    return render(request, "home.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_peca(request):
    if request.method == "GET":
        componentes = Componente.objects.all()
        return render(request, "add_peca.html")
    else:
        componente_id = request.POST.get("componente")
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        peca = Peca.objects.filter(nome=nome).first()
        if peca:
            return HttpResponse("Peça já existe")
        componente = get_object_or_404(Componente, id=componente_id)
        peca = Peca.objects.create(componente=componente, nome=nome, preco=preco)
        return HttpResponse("Peça cadastrada com sucesso!")
