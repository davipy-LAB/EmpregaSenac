from django.contrib import admin

from django.contrib import admin
from .models import Candidatura, Empresa, Vaga # O '.models' significa que ele busca no models.py do mesmo app

admin.site.register(Empresa)
admin.site.register(Vaga)
admin.site.register(Candidatura) # Registra Candidatura
# Register your models here.
