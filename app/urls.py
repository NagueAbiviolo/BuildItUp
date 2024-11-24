<<<<<<< HEAD
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
    path("editar/cpu/<int:pk>/", views.editar_cpu, name="editar_cpu"),
    path("editar/ram/<int:pk>/", views.editar_ram, name="editar_ram"),
    path("editar/hd/<int:pk>/", views.editar_hd, name="editar_hd"),
    path("editar/ssd/<int:pk>/", views.editar_ssd, name="editar_ssd"),
    path("editar/gpu/<int:pk>/", views.editar_gpu, name="editar_gpu"),
    path("editar/fonte/<int:pk>/", views.editar_fonte_alimentacao, name="editar_fonte"),
    path("editar/placa/<int:pk>/", views.editar_placa_mae, name="editar_placa"),
    path("editar/cooler/<int:pk>/", views.editar_cooler, name="editar_cooler"),
    path("editar/gabinete/<int:pk>/", views.editar_gabinete, name="editar_gabinete"),
    path("editar/ventoinha/<int:pk>/", views.editar_ventoinha, name="editar_ventoinha"),
    path("pecas/excluir/<int:peca_id>/", views.excluir_peca, name="excluir_peca"),
    path("meus_setups/", views.meus_setups, name="meus_setups"),
]
=======
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
    path("editar/cpu/<int:pk>/", views.editar_cpu, name="editar_cpu"),
    path("editar/ram/<int:pk>/", views.editar_ram, name="editar_ram"),
    path("editar/hd/<int:pk>/", views.editar_hd, name="editar_hd"),
    path("editar/ssd/<int:pk>/", views.editar_ssd, name="editar_ssd"),
    path("editar/gpu/<int:pk>/", views.editar_gpu, name="editar_gpu"),
    path("editar/fonte/<int:pk>/", views.editar_fonte_alimentacao, name="editar_fonte"),
    path("editar/placa/<int:pk>/", views.editar_placa_mae, name="editar_placa"),
    path("editar/cooler/<int:pk>/", views.editar_cooler, name="editar_cooler"),
    path("editar/gabinete/<int:pk>/", views.editar_gabinete, name="editar_gabinete"),
    path("editar/ventoinha/<int:pk>/", views.editar_ventoinha, name="editar_ventoinha"),
    path("pecas/excluir/<int:peca_id>/", views.excluir_peca, name="excluir_peca"),
    path("meus_setups/", views.meus_setups, name="meus_setups"),
]
>>>>>>> 0b70f733a5fbdca43ff5f98bde71b74d625c3dbb
