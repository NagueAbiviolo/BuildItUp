from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as login_django,
    logout as logout_django,
)
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
        return render(request, "home.html", {"pecas": pecas})
    else:
        nome = request.POST.get("setup_name")
        peca_ids = request.POST.getlist("pecas")

        setup = Setup(nome=nome)
        setup.save()
        setup.pecas.set(peca_ids)

        return redirect("home")


@login_required(login_url="/auth/login/")
def pecas(request):
    order = request.GET.get("order", "asc")
    pecas = Peca.objects.all()

    if order == "desc":
        pecas = pecas.order_by("-preco")
    else:
        pecas = pecas.order_by("preco")

    return render(request, "pecas.html", {"pecas": pecas, "order": order})


def add_ram(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        capacidade = request.POST["gb"]
        frequencia = request.POST["mhz"]
        ram = RAM(nome=nome, preco=preco, capacidade=capacidade, frequencia=frequencia)
        ram.save()
        return redirect("home")
    return render(request, "add_ram.html")


def add_hd(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        armazenamento = request.POST["armazenamento"]
        velocidade = request.POST["velocidade"]
        hd = HD(nome=nome, preco=preco, capacidade=armazenamento, velocidade=velocidade)
        hd.save()
        return redirect("home")
    return render(request, "add_hd.html")


def add_ssd(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        armazenamento = request.POST["armazenamento"]
        velocidade = request.POST["velocidade"]
        ssd = SSD(
            nome=nome, preco=preco, capacidade=armazenamento, velocidade=velocidade
        )
        ssd.save()
        return redirect("home")
    return render(request, "add_ssd.html")


def add_gpu(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        memoria = request.POST["memoria"]
        clock = request.POST["clock"]
        gpu = GPU(nome=nome, preco=preco, memoria=memoria, clock=clock)
        gpu.save()
        return redirect("home")
    return render(request, "add_gpu.html")


def add_cpu(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        nucleos = request.POST["nucleos"]
        clock = request.POST["clock"]
        cpu = CPU(nome=nome, preco=preco, nucleos=nucleos, clock=clock)
        cpu.save()
        return redirect("home")
    return render(request, "add_cpu.html")


def add_fonte(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        potencia = request.POST["potencia"]
        fonte = FonteAlimentacao(nome=nome, preco=preco, potencia=potencia)
        fonte.save()
        return redirect("home")
    return render(request, "add_fonte.html")


def add_placa_mae(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        socket = request.POST["socket"]
        formato = request.POST["formato"]
        chipset = request.POST["chipset"]
        placa_mae = PlacaMae(
            nome=nome, preco=preco, socket=socket, formato=formato, chipset=chipset
        )
        placa_mae.save()
        return redirect("home")
    return render(request, "add_placa_mae.html")


def add_cooler(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        tipo = request.POST["tipo"]
        tamanho = request.POST["tamanho"]
        cooler = Cooler(nome=nome, preco=preco, tipo=tipo, tamanho=tamanho)
        cooler.save()
        return redirect("home")
    return render(request, "add_cooler.html")


def add_gabinete(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        tipo = request.POST["tipo"]
        compatibilidade = request.POST["compatibilidade"]
        gabinete = Gabinete(
            nome=nome, preco=preco, tipo=tipo, compatibilidade=compatibilidade
        )
        gabinete.save()
        return redirect("home")
    return render(request, "add_gabinete.html")


def add_ventoinha(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        tamanho = request.POST["tamanho"]
        rpm = request.POST["rpm"]
        ventoinha = Ventoinha(nome=nome, preco=preco, tamanho=tamanho, rpm=rpm)
        ventoinha.save()
        return redirect("home")
    return render(request, "add_ventoinha.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_peca(request, peca_id):
    peca = get_object_or_404(Peca, id=peca_id)
    componente = None

    if isinstance(peca, RAM):
        componente = get_object_or_404(RAM, id=peca.id)
    elif isinstance(peca, HD):
        componente = get_object_or_404(HD, id=peca.id)
    elif isinstance(peca, SSD):
        componente = get_object_or_404(SSD, id=peca.id)
    elif isinstance(peca, GPU):
        componente = get_object_or_404(GPU, id=peca.id)
    elif isinstance(peca, CPU):
        componente = get_object_or_404(CPU, id=peca.id)
    elif isinstance(peca, FonteAlimentacao):
        componente = get_object_or_404(FonteAlimentacao, id=peca.id)
    elif isinstance(peca, PlacaMae):
        componente = get_object_or_404(PlacaMae, id=peca.id)
    elif isinstance(peca, Cooler):
        componente = get_object_or_404(Cooler, id=peca.id)
    elif isinstance(peca, Gabinete):
        componente = get_object_or_404(Gabinete, id=peca.id)
    elif isinstance(peca, Ventoinha):
        componente = get_object_or_404(Ventoinha, id=peca.id)

    if request.method == "GET":
        return render(
            request, "editar_peca.html", {"peca": peca, "componente": componente}
        )
    else:
        # Atualizar os campos específicos do componente com base no tipo
        if isinstance(componente, RAM):
            componente.gb = request.POST.get("gb")
            componente.mhz = request.POST.get("mhz")
        elif isinstance(componente, HD):
            componente.armazenamento = request.POST.get("armazenamento")
            componente.velocidade = request.POST.get("velocidade")
        elif isinstance(componente, SSD):
            componente.armazenamento = request.POST.get("armazenamento")
            componente.velocidade = request.POST.get("velocidade")
        elif isinstance(componente, GPU):
            componente.memoria = request.POST.get("memoria")
            componente.clock = request.POST.get("clock")
        elif isinstance(componente, CPU):
            componente.nucleos = request.POST.get("nucleos")
            componente.clock = request.POST.get("clock")
        elif isinstance(componente, FonteAlimentacao):
            componente.potencia = request.POST.get("potencia")
        elif isinstance(componente, PlacaMae):
            componente.formato = request.POST.get("formato")
            componente.chipset = request.POST.get("chipset")
        elif isinstance(componente, Cooler):
            componente.tipo = request.POST.get("tipo")
            componente.tamanho = request.POST.get("tamanho")
        elif isinstance(componente, Gabinete):
            componente.tipo = request.POST.get("tipo")
            componente.compatibilidade = request.POST.get("compatibilidade")
        elif isinstance(componente, Ventoinha):
            componente.tamanho = request.POST.get("tamanho")
            componente.rpm = request.POST.get("rpm")

        # Atualizar o nome e preço da peça
        peca.nome = request.POST.get("nome")
        peca.preco = request.POST.get("preco")
        componente.save()
        peca.save()

        return HttpResponseRedirect(reverse("pecas"))


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def excluir_peca(request, peca_id):
    peca = get_object_or_404(Peca, id=peca_id)
    peca.delete()
    return HttpResponseRedirect(reverse("pecas"))
