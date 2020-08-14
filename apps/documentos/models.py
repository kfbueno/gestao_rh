from django.db import models
from apps.funcionarios.models import Funcionario


# Create your models here.
class Documento(models.Model):
    descricao = models.CharField(max_length=100)
    pertence = models.ForeignKey(
    Funcionario, on_delete=models.PROTECT)
    arquivo = models.FileField(upload_to='documentos')  # quando fizer upload do arquivo vai para pasta documentos

    def get_absolute_url(self):
        return reverse('update_funcionario', args=[self.pertence.id])
    def __str__(self):
        return self.descricao
