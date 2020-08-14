from django.views.generic import ListView
from .models import RegistroHoraExtra


# Create your views here.
class HoraExtraList(ListView):
    model = RegistroHoraExtra

    def get_queryset(self):
        empresa_logada = self.request.user.funcionario.empresa
        return RegistroHoraExtra.objects.filter(funcionario__empresa=empresa_logada) #envia para o queryset o filtro desejado

