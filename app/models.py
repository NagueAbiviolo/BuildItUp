from django.db import models


# Classe base para Peças
class Peca(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


# Model para RAM
class RAM(Peca):
    gb = models.IntegerField()  # Capacidade em GB
    mhz = models.IntegerField()  # Frequência em MHz

    def __str__(self):
        return f"{self.nome} - {self.gb}GB - {self.mhz}MHz"


# Model para HD
class HD(Peca):
    armazenamento = models.IntegerField()  # Capacidade em GB
    velocidade = models.IntegerField()  # Velocidade em RPM

    def __str__(self):
        return f"{self.nome} - {self.armazenamento}GB - {self.velocidade}RPM"


# Model para SSD
class SSD(Peca):
    armazenamento = models.IntegerField()  # Capacidade em GB
    velocidade = models.IntegerField()  # Velocidade em MB/s

    def __str__(self):
        return f"{self.nome} - {self.armazenamento}GB - {self.velocidade}MB/s"


# Model para GPU
class GPU(Peca):
    memoria = models.IntegerField()  # Capacidade em GB
    clock = models.IntegerField()  # Velocidade em MHz

    def __str__(self):
        return f"{self.nome} - {self.memoria}GB - {self.clock}MHz"


# Model para CPU
class CPU(Peca):
    nucleos = models.IntegerField()  # Número de núcleos
    clock = models.FloatField()  # Frequência em GHz
    chipset = models.CharField(max_length=100, null = True)
    def __str__(self):
        return f"{self.nome} - {self.nucleos} Núcleos - {self.clock}GHz"


# Model para Fonte de Alimentação
class FonteAlimentacao(Peca):
    potencia = models.IntegerField()  # Potência em Watts

    def __str__(self):
        return f"{self.nome} - {self.potencia}W"


# Model para Placa Mãe
class PlacaMae(Peca):
    formato = models.CharField(max_length=50)  # ATX, Micro-ATX, Mini-ITX
    chipset = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.formato} - {self.chipset}"


# Model para Cooler
class Cooler(Peca):
    tipo = models.CharField(max_length=50, default="Ar")  # Default value for tipo
    tamanho = models.CharField(max_length=50, default="120mm")  # Example default

    def __str__(self):
        return f"{self.nome} - {self.tipo} - {self.tamanho}"


# Model para Gabinete
class Gabinete(Peca):
    tipo = models.CharField(max_length=50)  # ATX, Micro-ATX, etc.
    compatibilidade = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.tipo} - {self.compatibilidade}"


# Model para Ventoinha
class Ventoinha(Peca):
    tamanho = models.IntegerField()  # em mm
    rpm = models.IntegerField()  # Rotação por minuto

    def __str__(self):
        return f"{self.nome} - {self.tamanho}mm - {self.rpm}RPM"


# Model para Setup
class Setup(models.Model):
    nome = models.CharField(max_length=100)
    pecas = models.ManyToManyField(Peca)  # Agora relaciona diretamente com Peca

    def __str__(self):
        return self.nome
