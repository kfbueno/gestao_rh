from django.db import models
from django.contrib.auth.models import User
from apps.departamentos.models import Departamentos   # um usuario pode estar em multiplos departamentos
from apps.empresas.models import Empresa
from django.urls import reverse

# Create your models here.
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.PROTECT)    # Protect nao apaga em cascata
    departamentos = models.ManyToManyField(Departamentos)   # foreingkey de um para n
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('list_funcionarios')

    def __str__(self):
        return self.nome