from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User
from .models import Funcionario

# Create your views here.


class FuncionariosList(ListView):
    model = Funcionario

    '''
        reescreve ou subscreve uma funcao ja existente do django onde devera retornar somente os 
        funconarios referentes a empresa logada
    '''

    def get_queryset(self):
        empresa_logada = self.request.user.funcionario.empresa
        return Funcionario.objects.filter(empresa=empresa_logada) #envia para o queryset o filtro desejado


class FuncionarioEdit(UpdateView):
    model = Funcionario
    fields = ['nome', 'departamentos']


class FuncionarioDelete(DeleteView):
    model = Funcionario
    success_url = reverse_lazy('list_funcionarios')


class FuncionarioNovo(CreateView):
    model = Funcionario
    fields = ['nome', 'departamentos']

    # redefino o methodo do django
    def form_valid(self, form):
        funcionario =  form.save(commit=False) #somente cria o objeto em memoria e nao no banco
        #username do usuario sugerido
        username = funcionario.nome.split(' ')[0] + funcionario.nome.split(' ')[1]

        #defino a empresa do funcionario
        funcionario.empresa = self.request.user.funcionario.empresa
        #crio um usuario para este funcionario
        funcionario.user = User.objects.create(username= username)
        funcionario.save()
        return super(FuncionarioNovo, self).form_valid(form)



