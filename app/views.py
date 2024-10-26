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
    if request.method == "GET":
        pecas = Peca.objects.all()
        componentes = Componente.objects.all()
        componentes_dict = {}
        for componente in componentes:
            componentes_dict[componente.nome] = Peca.objects.filter(componente=componente)
        return render(
            request, "home.html", {"pecas": pecas, "componentes": componentes_dict}
        )

    else:
        nome = request.POST.get("setup_name")
        peca_ids = request.POST.getlist("pecas")

        setup = Setup(nome=nome)
        setup.save()
        setup.pecas.set(peca_ids)

        return redirect("home")


@login_required(login_url="/auth/login/")
def pecas(request):
    componente_id = request.GET.get("componente")
    order = request.GET.get("order", "asc")
    if componente_id:
        pecas = Peca.objects.filter(componente_id=componente_id)
    else:
        pecas = Peca.objects.all()

    if order == "desc":
        pecas = pecas.order_by("-preco")
    else:
        pecas = pecas.order_by("preco")

    componentes = Componente.objects.all()

    return render(
        request,
        "pecas.html",
        {
            "pecas": pecas,
            "componentes": componentes,
            "componente_selecionado": componente_id,
            "order": order,
        },
    )


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_peca(request):
    if request.method == "GET":
        componentes = Componente.objects.all()
        return render(request, "add_peca.html", {"componentes": componentes})

    else:
        componente_id = request.POST.get("componente")
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        peca = Peca.objects.filter(nome=nome).first()
        if peca:
            return HttpResponse("Peça já existe")
        componente = get_object_or_404(Componente, id=componente_id)
        peca = Peca.objects.create(componente=componente, nome=nome, preco=preco)
        return HttpResponseRedirect(reverse("pecas"))


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_peca(request, peca_id):
    peca = get_object_or_404(Peca, id=peca_id)
    if request.method == "GET":
        componentes = Componente.objects.all()
        return render(
            request, "editar_peca.html", {"peca": peca, "componentes": componentes}
        )
    else:
        componente_id = request.POST.get("componente")
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        componente = get_object_or_404(Componente, id=componente_id)
        peca.componente = componente
        peca.nome = nome
        peca.preco = preco
        peca.save()
        return HttpResponseRedirect(reverse("pecas"))


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def excluir_peca(request, peca_id):
    peca = get_object_or_404(Peca, id=peca_id)
    peca.delete()
    return HttpResponseRedirect(reverse("pecas"))
