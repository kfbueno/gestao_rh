from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.funcionarios.models import Funcionario    #importo para identificar o funcionario que vai logar


# Create your views here.
@login_required #impede que acesse o sistema sem estar logado
def home(request):
    data = {}
    data['usuario'] = request.user
    return render(request, 'core/index.html', data)