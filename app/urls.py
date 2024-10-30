from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("pecas/", views.pecas, name="pecas"),
    path("add_ram/", views.add_ram, name="add_ram"),
    path("add_hd/", views.add_hd, name="add_hd"),
    path("add_ssd/", views.add_ssd, name="add_ssd"),
    path("add_gpu/", views.add_gpu, name="add_gpu"),
    path("add_cpu/", views.add_cpu, name="add_cpu"),
    path("add_fonte/", views.add_fonte, name="add_fonte"),
    path("add_placa_mae/", views.add_placa_mae, name="add_placa_mae"),
    path("add_cooler/", views.add_cooler, name="add_cooler"),
    path("add_gabinete/", views.add_gabinete, name="add_gabinete"),
    path("add_ventoinha/", views.add_ventoinha, name="add_ventoinha"),
]
