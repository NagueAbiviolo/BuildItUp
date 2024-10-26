from django.db import models


class Componente(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Peca(models.Model):
    nome = models.CharField(max_length=100)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class Setup(models.Model):
    nome = models.CharField(max_length=100)
    pecas = models.ManyToManyField(Peca, related_name="Peças")
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.preco = sum(peca.preco for peca in self.pecas.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
