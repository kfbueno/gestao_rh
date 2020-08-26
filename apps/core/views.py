from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario    #importo para identificar o funcionario que vai logar

# importações do restframework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apps.core.serializers import UserSerializer, GroupSerializer

# para o celery
from .tasks import send_relatorio

# Create your views here.
@login_required #impede que acesse o sistema sem estar logado
def home(request):
    data = {}
    data['usuario'] = request.user
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

