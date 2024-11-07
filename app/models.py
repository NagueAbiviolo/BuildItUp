from django.db import models


class Peca(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class RAM(Peca):
    gb = models.IntegerField()
    mhz = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.gb}GB - {self.mhz}MHz"


class HD(Peca):
    armazenamento = models.IntegerField()
    velocidade = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.armazenamento}GB - {self.velocidade}RPM"


class SSD(Peca):
    armazenamento = models.IntegerField()
    velocidade = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.armazenamento}GB - {self.velocidade}MB/s"


class GPU(Peca):
    memoria = models.IntegerField()
    clock = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.memoria}GB - {self.clock}MHz"


class CPU(Peca):
    nucleos = models.IntegerField()
    clock = models.FloatField()
    chipset = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.nome} - {self.nucleos} Núcleos - {self.clock}GHz"


class FonteAlimentacao(Peca):
    potencia = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.potencia}W"


class PlacaMae(Peca):
    formato = models.CharField(max_length=50)
    chipset = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.formato} - {self.chipset}"


class Cooler(Peca):
    tipo = models.CharField(max_length=50, default="Ar")
    tamanho = models.CharField(max_length=50, default="120mm")

    def __str__(self):
        return f"{self.nome} - {self.tipo} - {self.tamanho}"


class Gabinete(Peca):
    tipo = models.CharField(max_length=50)
    compatibilidade = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.tipo} - {self.compatibilidade}"


class Ventoinha(Peca):
    tamanho = models.IntegerField()
    rpm = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - {self.tamanho}mm - {self.rpm}RPM"


class Setup(models.Model):
    nome = models.CharField(max_length=100)
    pecas = models.ManyToManyField(Peca)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome
