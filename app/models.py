from django.db import models

# app/models.py
from django.db import models
from django.contrib.auth.models import User # Aqui eu importo o modelo User do Django

# Modelo para a Empresa
class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa_profile')
    nome_fantasia = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição da Empresa")
    site = models.URLField(blank=True, null=True, verbose_name="Site da Empresa")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome_fantasia

# Modelo para a Vaga de Emprego
class Vaga(models.Model):
    NIVEL_CHOICES = [
        ('estagio', 'Estágio'),
        ('junior', 'Júnior'),
        ('pleno', 'Pleno'),
        ('senior', 'Sênior'),
        ('especialista', 'Especialista'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vagas')
    titulo = models.CharField(max_length=255, verbose_name="Título da Vaga")
    descricao = models.TextField(verbose_name="Descrição da Vaga")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, verbose_name="Nível")
    localidade = models.CharField(max_length=100, verbose_name="Localidade")
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salário")
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")
    ativa = models.BooleanField(default=True, verbose_name="Vaga Ativa")

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"
        ordering = ['-data_publicacao']

    def __str__(self):
        return f"{self.titulo} ({self.empresa.nome_fantasia})"
# Create your models here.

class Candidatura(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidaturas')
    nome_candidato = models.CharField(max_length=100)
    email_candidato = models.EmailField()
    curriculo = models.FileField(upload_to='curriculos/') # Onde os arquivos serão armazenados
    data_candidatura = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        ordering = ['-data_candidatura'] # Ordena as candidaturas pelas mais recentes

    def __str__(self):
        return f"Candidatura de {self.nome_candidato} para {self.vaga.titulo}"