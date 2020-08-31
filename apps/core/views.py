from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario    #importo para identificar o funcionario que vai logar

# importações do restframework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apps.core.serializers import UserSerializer, GroupSerializer

from apps.registro_hora_extra.models import RegistroHoraExtra
from apps.departamentos.models import Departamentos

# para o celery
from .tasks import send_relatorio
from django.db.models import Sum

from django.core import serializers
from django.http import HttpResponse

# Create your views here.
@login_required #impede que acesse o sistema sem estar logado
def home(request):
    data = {}
    data['usuario'] = request.user
    funcionario = request.user.funcionario
    data['total funcionarios'] = funcionario.empresa.total_funcionarios
    data['total funcionarios ferias'] = funcionario.empresa.total_funcionarios_ferias
    data['total funcionarios doc pendentes'] = funcionario.empresa.total_funcionario_doc_pendente
    data['total_funcionarios_doc_ok'] = funcionario.empresa.total_funcionarios_doc_ok
    data['total_funcionarios_rg'] = 10
    data['total_hora_extra_utilizadas'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=True).aggregate(Sum('horas'))['horas__sum'] or 0
    data['total_hora_extra_pendente'] = RegistroHoraExtra.objects.filter(
        funcionario__empresa=funcionario.empresa, utilizada=False).aggregate(Sum('horas'))['horas__sum'] or 0
    return render(request, 'core/index.html', data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def celery(request):
    send_relatorio.delay()
    #send_relatorio() para servidor windows nao utilizar delay
    return HttpResponse('Tarefa incluida na fila para execução')

def departamentos_ajax(request):
    departamentos = Departamentos.objects.all()
    return render(request, 'departamentos_ajax.html', {'departamentos': departamentos})

def filtra_funcionarios(request):
    depart = request.GET['outro_param']
    departamento = Departamentos.objects.get(id=depart)

    qs_json = serializers.serialize('json', departamento.funcionario_set.all())
    return HttpResponse(qs_json, content_type='application/json')
