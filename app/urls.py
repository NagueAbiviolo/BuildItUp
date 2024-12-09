from django.urls import path
from . import views
from .models import (
    RAM,
    HD,
    SSD,
    GPU,
    CPU,
    FonteAlimentacao,
    PlacaMae,
    Cooler,
    Gabinete,
    Ventoinha,
)

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("pecas/", views.pecas, name="pecas"),
    path("meus_setups/", views.meus_setups, name="meus_setups"),
    path("pecas/excluir/<int:peca_id>/", views.excluir_peca, name="excluir_peca"),
    # Adicionar peças
    path(
        "add_ram/",
        views.add_peca,
        {"model": RAM, "template_name": "add_peca.html"},
        name="add_ram",
    ),
    path(
        "add_hd/",
        views.add_peca,
        {"model": HD, "template_name": "add_peca.html"},
        name="add_hd",
    ),
    path(
        "add_ssd/",
        views.add_peca,
        {"model": SSD, "template_name": "add_peca.html"},
        name="add_ssd",
    ),
    path(
        "add_gpu/",
        views.add_peca,
        {"model": GPU, "template_name": "add_peca.html"},
        name="add_gpu",
    ),
    path(
        "add_cpu/",
        views.add_peca,
        {"model": CPU, "template_name": "add_peca.html"},
        name="add_cpu",
    ),
    path(
        "add_fonte/",
        views.add_peca,
        {"model": FonteAlimentacao, "template_name": "add_peca.html"},
        name="add_fonte",
    ),
    path(
        "add_placa_mae/",
        views.add_peca,
        {"model": PlacaMae, "template_name": "add_peca.html"},
        name="add_placa_mae",
    ),
    path(
        "add_cooler/",
        views.add_peca,
        {"model": Cooler, "template_name": "add_peca.html"},
        name="add_cooler",
    ),
    path(
        "add_gabinete/",
        views.add_peca,
        {"model": Gabinete, "template_name": "add_peca.html"},
        name="add_gabinete",
    ),
    path(
        "add_ventoinha/",
        views.add_peca,
        {"model": Ventoinha, "template_name": "add_peca.html"},
        name="add_ventoinha",
    ),
    # Editar peças
    path(
        "editar/cpu/<int:pk>/",
        views.editar_peca,
        {"model": CPU, "template_name": "editar_peca.html"},
        name="editar_cpu",
    ),
    path(
        "editar/ram/<int:pk>/",
        views.editar_peca,
        {"model": RAM, "template_name": "editar_peca.html"},
        name="editar_ram",
    ),
    path(
        "editar/hd/<int:pk>/",
        views.editar_peca,
        {"model": HD, "template_name": "editar_peca.html"},
        name="editar_hd",
    ),
    path(
        "editar/ssd/<int:pk>/",
        views.editar_peca,
        {"model": SSD, "template_name": "editar_peca.html"},
        name="editar_ssd",
    ),
    path(
        "editar/gpu/<int:pk>/",
        views.editar_peca,
        {"model": GPU, "template_name": "editar_peca.html"},
        name="editar_gpu",
    ),
    path(
        "editar/fonte/<int:pk>/",
        views.editar_peca,
        {"model": FonteAlimentacao, "template_name": "editar_peca.html"},
        name="editar_fonte",
    ),
    path(
        "editar/placa/<int:pk>/",
        views.editar_peca,
        {"model": PlacaMae, "template_name": "editar_peca.html"},
        name="editar_placa",
    ),
    path(
        "editar/cooler/<int:pk>/",
        views.editar_peca,
        {"model": Cooler, "template_name": "editar_peca.html"},
        name="editar_cooler",
    ),
    path(
        "editar/gabinete/<int:pk>/",
        views.editar_peca,
        {"model": Gabinete, "template_name": "editar_peca.html"},
        name="editar_gabinete",
    ),
    path(
        "editar/ventoinha/<int:pk>/",
        views.editar_peca,
        {"model": Ventoinha, "template_name": "editar_peca.html"},
        name="editar_ventoinha",
    ),
    path("editar_setup/<int:setup_id>/", views.editar_setup, name="editar_setup"),
    path("excluir_setup/<int:setup_id>/", views.excluir_setup, name="excluir_setup"),
]
