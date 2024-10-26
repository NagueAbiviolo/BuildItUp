from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("pecas/", views.pecas, name="pecas"),
    path("add_peca/", views.add_peca, name="add_peca"),
    path("editar_peca/<int:peca_id>/", views.editar_peca, name="editar_peca"),
    path("pecas/excluir/<int:peca_id>/", views.excluir_peca, name="excluir_peca"),
]
