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
        if User.objects.filter(username=username).exists():
            return HttpResponse("Já existe um usuário com esse username")
        User.objects.create_user(username=username, email=email, password=senha)
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
        return HttpResponse("Usuário ou senha inválidos")


def logout(request):
    logout_django(request)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/auth/login/")
def home(request):
    if request.method == "GET":
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

        setups = Setup.objects.filter(user=request.user)
        setup_atual = setups.first()
        tdp_total = setup_atual.tdp_total if setup_atual else 0
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
                {
                    "error": "Nome do setup ou peças não fornecidos.",
                    "componentes": {
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
                    },
                },
            )

        pecas_com_quantidades = pecas_selecionadas.split(",")
        peca_ids = []
        ram_quantities = {}

        for peca in pecas_com_quantidades:
            if ":" in peca:
                peca_id, quantidade = peca.split(":")
                peca_id = int(peca_id)
                quantidade = int(quantidade)
                ram_quantities[peca_id] = quantidade
            else:
                peca_id = int(peca)
            peca_ids.append(peca_id)

        pecas = Peca.objects.filter(id__in=peca_ids)
        if not pecas.exists():
            return render(
                request,
                "home.html",
                {
                    "error": "Nenhuma peça encontrada com os IDs fornecidos.",
                    "componentes": {
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
                    },
                },
            )

        preco_total = 0
        tdp_total = 0

        for peca in pecas:
            quantidade = ram_quantities.get(peca.id, 1)
            preco_total += peca.preco * quantidade
            tdp_total += peca.tdp * quantidade

        cpu = CPU.objects.filter(id__in=pecas.values_list("id", flat=True)).first()
        placa_mae = PlacaMae.objects.filter(
            id__in=pecas.values_list("id", flat=True)
        ).first()
        if cpu and placa_mae and cpu.socket != placa_mae.socket:
            return render(
                request,
                "home.html",
                {
                    "error": f"Incompatibilidade entre o socket da Placa-Mãe ({placa_mae.socket}) e do CPU ({cpu.socket}).",
                    "componentes": {
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
                    },
                },
            )

        fonte = FonteAlimentacao.objects.filter(
            id__in=pecas.values_list("id", flat=True)
        ).first()
        if fonte and fonte.potencia < tdp_total:
            return render(
                request,
                "home.html",
                {
                    "error": f"A fonte selecionada ({fonte.nome}) não tem potência suficiente para o TDP total do setup ({tdp_total}W).",
                    "componentes": {
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
                    },
                },
            )

        setup = Setup.objects.create(
            nome=nome, preco=preco_total, tdp_total=tdp_total, user=request.user
        )
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

    if componente_selecionado:
        pecas = pecas.filter(tipo=componente_selecionado)

    pecas = pecas.order_by("-preco" if order == "desc" else "preco")

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
def add_peca(request, model, template_name):
    if request.method == "POST":
        fields = {}
        for field in model._meta.fields:
            if field.name in request.POST:
                fields[field.name] = request.POST.get(field.name, "")
        model.objects.create(**fields)
        return redirect("home")

    fields = [
        {"name": field.name, "label": field.verbose_name, "value": ""}
        for field in model._meta.fields
        if field.name != "id" and not field.auto_created
    ]

    return render(request, template_name, {"fields": fields})


from django.db.models import DecimalField


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_peca(request, model, pk, template_name):
    peca = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        for field in model._meta.fields:
            if field.name in request.POST:
                setattr(peca, field.name, request.POST[field.name])
        peca.save()
        return redirect("pecas")

    fields = [
        {
            "name": field.name,
            "label": field.verbose_name,
            "value": (
                format(getattr(peca, field.name), ".2f").replace(",", ".")
                if isinstance(getattr(peca, field.name), (float, DecimalField))
                else getattr(peca, field.name)
            ),
        }
        for field in model._meta.fields
        if field.name != "id" and not field.auto_created
    ]

    # Ajuste específico para o campo preco
    for field in fields:
        if field["name"] == "preco":
            field["value"] = str(field["value"]).replace(",", ".")

    return render(request, template_name, {"fields": fields})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def excluir_peca(request, peca_id):
    peca = get_object_or_404(Peca, id=peca_id)
    peca.delete()
    return HttpResponseRedirect(reverse("pecas"))


@login_required(login_url="/auth/login/")
def meus_setups(request):
    setups = Setup.objects.filter(user=request.user)
    setups_com_quantidades = []

    for setup in setups:
        quantidades = {}
        for peca in setup.pecas.all():
            if isinstance(peca, RAM):
                quantidade = setup.pecas.filter(id=peca.id).count()
                quantidades[peca.id] = quantidade
        setups_com_quantidades.append((setup, quantidades))

    context = {
        "setups_com_quantidades": setups_com_quantidades,
    }
    return render(request, "meus_setups.html", context)


@login_required(login_url="/auth/login/")
def editar_setup(request, setup_id):
    setup = get_object_or_404(Setup, id=setup_id, user=request.user)

    if request.method == "POST":
        nome = request.POST.get("setup_name")

        if not nome:
            return render(
                request,
                "editar_setup.html",
                {
                    "setup": setup,
                    "error": "Nome do setup não fornecido.",
                },
            )

        setup.nome = nome
        setup.save()

        return redirect("meus_setups")

    return render(request, "editar_setup.html", {"setup": setup})


@login_required
def excluir_setup(request, setup_id):
    setup = get_object_or_404(Setup, id=setup_id, user=request.user)

    if request.method == "POST":
        setup.delete()
        return redirect("meus_setups")

    return render(request, "excluir_setup.html", {"setup": setup})
