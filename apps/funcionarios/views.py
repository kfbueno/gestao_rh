import io

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas

from .models import Funcionario

# para geracao de relatorio pdf a partir de html

from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

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

def relatorio_funcionarios(request):
    response = HttpResponse(content_type='application/pdf')

    # para baixar o relatorio (download) quando clicado no link
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'

    # obrigatorio criar o buffer e objeto canvas
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # escrevendo no relatorio coordenadas y e x... tipo @say
    p.drawString(200, 810, 'Relatório de Funcionários')

    # fazendo uma query para buscar o cadastro de funcionarios (all)
    # funcionarios = Funcionario.objects.all()

    # filtrando uma query por empresa. Passa o where para a query
    funcionarios = Funcionario.objects.filter(empresa=request.user.funcionario.empresa)

    str_ = 'Nome: %s | Hora Extra: %.2f'

    # construindo linha abaixo do titulo
    p.drawString(0, 800, '_' * 150)

    y = 750
    for funcionario in funcionarios:
        p.drawString(10, y, str_ % (funcionario.nome, funcionario.total_horas_extra))
        y -= 20

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode("UTF-8")), response)

        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)


class Pdf(View):

    def get(self, request):
        params = {
            'today': 'Variavel today',
            'sales': 'Variavel Sales',
            'request': request,
        }
        return Render.render('funcionarios/relatorio.html', params, 'myfile')
