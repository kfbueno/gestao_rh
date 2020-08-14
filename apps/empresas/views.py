from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from .models import Empresa

# Create your views here.
class EmpresaCreate(CreateView):
    model = Empresa
    fields = ['nome']

    '''
        subscreve a funcao form_valid, assim que o form for validado 
        pegamos o objeto que esta sendo criado, no caso a empresa, pegar o usuario que esta sendo
        cadastrado e vincular o funcinario com a empresa
    '''
    def form_valid(self, form):
        obj = form.save()   # instancia obj com a empresa
        funcionario = self.request.user.funcionario # atribui a funcionario o funcionaro logado
        funcionario.empresa = obj
        funcionario.save()
        return HttpResponse('ok')

class EmpresaEdit(UpdateView):
    model = Empresa
    fields = ['nome']

