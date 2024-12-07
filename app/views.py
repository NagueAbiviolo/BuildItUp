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
from django.db.models import Case, When, Value, CharField, Sum


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
        # Obter peças por categoria
        pecas_por_categoria = {
            "RAM": RAM.objects.all(),
            "HD": HD.objects.all(),
            "SSD": SSD.objects.all(),
            "GPU": GPU.objects.all(),
            "CPU": CPU.objects.all(),
            "Fonte de Alimentacao": FonteAlimentacao.objects.all(),
            "Placa Mae": PlacaMae.objects.all(),
            "Cooler": Cooler.objects.all(),
            "Gabinete": Gabinete.objects.all(),
            "Ventoinha": Ventoinha.objects.all(),
        }

        # Obter o setup do usuário
        setups = Setup.objects.filter(user=request.user)
        setup_atual = setups.first()

        # Calcular o TDP total
        tdp_total = 0
        if setup_atual:
            tdp_total = setup_atual.tdp_total  # Já calculado previamente

        # Buscar fontes compatíveis
        fontes_compativeis = FonteAlimentacao.objects.filter(
            potencia__gte=tdp_total + 50
        )

        context = {
            "componentes": pecas_por_categoria,
            "setup_atual": setup_atual,
            "tdp_total": tdp_total,
            "fontes_compativeis": fontes_compativeis,
        }
        return render(request, "home.html", context)

    elif request.method == "POST":
        nome = request.POST.get("setup_name")
        pecas_selecionadas = request.POST.get("pecas", "")

        if not nome or not pecas_selecionadas:
            return render(
                request,
                "home.html",
                {"error": "Nome do setup ou peças não fornecidos."},
            )

        # Converte a string com IDs separados por vírgulas para uma lista de inteiros
        try:
            peca_ids = [int(id) for id in pecas_selecionadas.split(",")]
        except ValueError:
            return render(request, "home.html", {"error": "IDs das peças inválidos."})

        # Busca as peças selecionadas no banco de dados
        pecas = Peca.objects.filter(id__in=peca_ids)

        if not pecas.exists():
            return render(
                request,
                "home.html",
                {"error": "Nenhuma peça encontrada com os IDs fornecidos."},
            )

        # Calcular o preço total e TDP total das peças selecionadas
        preco_total = pecas.aggregate(total_preco=Sum("preco"))["total_preco"] or 0
        tdp_total = pecas.aggregate(total_tdp=Sum("tdp"))["total_tdp"] or 0

        # Criar o setup
        setup = Setup.objects.create(
            nome=nome, preco=preco_total, tdp_total=tdp_total, user=request.user
        )

        # Adicionar as peças ao setup
        setup.pecas.set(pecas)

        return redirect("meus_setups")

    return render(request, "home.html")


@login_required(login_url="/auth/login/")
def pecas(request):
    order = request.GET.get("order", "asc")
    componente_selecionado = request.GET.get("componente", "")

    pecas = Peca.objects.annotate(
        tipo=Case(
            When(ram__isnull=False, then=Value("RAM")),
            When(hd__isnull=False, then=Value("HD")),
            When(ssd__isnull=False, then=Value("SSD")),
            When(gpu__isnull=False, then=Value("GPU")),
            When(cpu__isnull=False, then=Value("CPU")),
            When(fontealimentacao__isnull=False, then=Value("Fonte de Alimentação")),
            When(placamae__isnull=False, then=Value("Placa Mãe")),
            When(cooler__isnull=False, then=Value("Cooler")),
            When(gabinete__isnull=False, then=Value("Gabinete")),
            When(ventoinha__isnull=False, then=Value("Ventoinha")),
            default=Value("Desconhecido"),
            output_field=CharField(),
        )
    )

    # Aplicar o filtro por componente, se um foi selecionado
    if componente_selecionado:
        pecas = pecas.filter(tipo=componente_selecionado)

    # Ordenar pelo preço
    if order == "desc":
        pecas = pecas.order_by("-preco")
    else:
        pecas = pecas.order_by("preco")

    # Listar os tipos únicos de componentes para o dropdown no template
    tipos_componentes = [
        "RAM",
        "HD",
        "SSD",
        "GPU",
        "CPU",
        "Fonte de Alimentação",
        "Placa Mãe",
        "Cooler",
        "Gabinete",
        "Ventoinha",
    ]

    return render(
        request,
        "pecas.html",
        {
            "pecas": pecas,
            "order": order,
            "componentes": tipos_componentes,
            "componente_selecionado": componente_selecionado,
        },
    )


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_ram(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        capacidade = request.POST["gb"]
        frequencia = request.POST["mhz"]
        ram = RAM(nome=nome, preco=preco, gb=capacidade, mhz=frequencia)
        ram.save()
        return redirect("home")
    return render(request, "add_ram.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_hd(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        armazenamento = request.POST["armazenamento"]
        velocidade = request.POST["velocidade"]
        hd = HD(
            nome=nome, preco=preco, armazenamento=armazenamento, velocidade=velocidade
        )
        hd.save()
        return redirect("home")
    return render(request, "add_hd.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_ssd(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        armazenamento = request.POST["armazenamento"]
        velocidade = request.POST["velocidade"]
        ssd = SSD(
            nome=nome, preco=preco, armazenamento=armazenamento, velocidade=velocidade
        )
        ssd.save()
        return redirect("home")
    return render(request, "add_ssd.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
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


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
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


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_fonte(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        potencia = request.POST["potencia"]
        fonte = FonteAlimentacao(nome=nome, preco=preco, potencia=potencia)
        fonte.save()
        return redirect("home")
    return render(request, "add_fonte.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_placa_mae(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        formato = request.POST["formato"]
        chipset = request.POST["chipset"]
        placa_mae = PlacaMae(nome=nome, preco=preco, formato=formato, chipset=chipset)
        placa_mae.save()
        return redirect("home")
    return render(request, "add_placa_mae.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
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


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_gabinete(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        preco = request.POST["preco"]
        tipo = request.POST["tipo"]
        gabinete = Gabinete(
            nome=nome,
            preco=preco,
            tipo=tipo,
        )
        gabinete.save()
        return redirect("home")
    return render(request, "add_gabinete.html")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
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
def editar_cpu(request, pk):
    cpu = get_object_or_404(CPU, pk=pk)
    if request.method == "POST":
        cpu.nome = request.POST.get("nome")
        cpu.preco = request.POST.get("preco")
        cpu.nucleos = request.POST.get("nucleos")
        cpu.clock = request.POST.get("clock")
        cpu.chipset = request.POST.get("chipset")
        cpu.save()
        return redirect("pecas")
    return render(request, "editar_cpu.html", {"cpu": cpu})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_ram(request, pk):
    ram = get_object_or_404(RAM, pk=pk)
    if request.method == "POST":
        ram.nome = request.POST.get("nome")
        ram.preco = request.POST.get("preco")
        ram.gb = request.POST.get("gb")
        ram.mhz = request.POST.get("mhz")
        ram.save()
        return redirect("pecas")
    return render(request, "editar_ram.html", {"ram": ram})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_hd(request, pk):
    hd = get_object_or_404(HD, pk=pk)
    if request.method == "POST":
        hd.nome = request.POST.get("nome")
        hd.preco = request.POST.get("preco")
        hd.armazenamento = request.POST.get("armazenamento")
        hd.velocidade = request.POST.get("velocidade")
        hd.save()
        return redirect("pecas")
    return render(request, "editar_hd.html", {"hd": hd})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_ssd(request, pk):
    ssd = get_object_or_404(SSD, pk=pk)
    if request.method == "POST":
        ssd.nome = request.POST.get("nome")
        ssd.preco = request.POST.get("preco")
        ssd.armazenamento = request.POST.get("armazenamento")
        ssd.velocidade = request.POST.get("velocidade")
        ssd.save()
        return redirect("pecas")
    return render(request, "editar_ssd.html", {"ssd": ssd})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_gpu(request, pk):
    gpu = get_object_or_404(GPU, pk=pk)
    if request.method == "POST":
        gpu.nome = request.POST.get("nome")
        gpu.preco = request.POST.get("preco")
        gpu.memoria = request.POST.get("memoria")
        gpu.clock = request.POST.get("clock")
        gpu.save()
        return redirect("pecas")
    return render(request, "editar_gpu.html", {"gpu": gpu})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_fonte_alimentacao(request, pk):
    fonte = get_object_or_404(FonteAlimentacao, pk=pk)
    if request.method == "POST":
        fonte.nome = request.POST.get("nome")
        fonte.preco = request.POST.get("preco")
        fonte.potencia = request.POST.get("potencia")
        fonte.save()
        return redirect("pecas")
    return render(request, "editar_fonte.html", {"fonte": fonte})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_placa_mae(request, pk):
    placa = get_object_or_404(PlacaMae, pk=pk)
    if request.method == "POST":
        placa.nome = request.POST.get("nome")
        placa.preco = request.POST.get("preco")
        placa.formato = request.POST.get("formato")
        placa.chipset = request.POST.get("chipset")
        placa.save()
        return redirect("pecas")
    return render(request, "editar_placa.html", {"placa": placa})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_cooler(request, pk):
    cooler = get_object_or_404(Cooler, pk=pk)
    if request.method == "POST":
        cooler.nome = request.POST.get("nome")
        cooler.preco = request.POST.get("preco")
        cooler.tipo = request.POST.get("tipo")
        cooler.tamanho = request.POST.get("tamanho")
        cooler.save()
        return redirect("pecas")
    return render(request, "editar_cooler.html", {"cooler": cooler})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_gabinete(request, pk):
    gabinete = get_object_or_404(Gabinete, pk=pk)
    if request.method == "POST":
        gabinete.nome = request.POST.get("nome")
        gabinete.preco = request.POST.get("preco")
        gabinete.tipo = request.POST.get("tipo")
        gabinete.compatibilidade = request.POST.get("compatibilidade")
        gabinete.save()
        return redirect("pecas")
    return render(request, "editar_gabinete.html", {"gabinete": gabinete})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_ventoinha(request, pk):
    ventoinha = get_object_or_404(Ventoinha, pk=pk)
    if request.method == "POST":
        ventoinha.nome = request.POST.get("nome")
        ventoinha.preco = request.POST.get("preco")
        ventoinha.tamanho = request.POST.get("tamanho")
        ventoinha.rpm = request.POST.get("rpm")
        ventoinha.save()
        return redirect("pecas")
    return render(request, "editar_ventoinha.html", {"ventoinha": ventoinha})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def excluir_peca(request, peca_id):
    peca = get_object_or_404(Peca, id=peca_id)
    peca.delete()
    return HttpResponseRedirect(reverse("pecas"))


@login_required(login_url="/auth/login/")
def meus_setups(request):
    if not request.user.is_authenticated:
        return redirect("login")

    setups = Setup.objects.filter(user=request.user)
    return render(request, "meus_setups.html", {"setups": setups})
