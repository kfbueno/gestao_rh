from django.urls import path
from .views import (
    FuncionariosList,
    FuncionarioEdit,
    FuncionarioDelete,
    FuncionarioNovo,
    Pdf
)

from .views import relatorio_funcionarios

urlpatterns = [
    path('', FuncionariosList.as_view(), name='list_funcionarios'),
    path('editar/<int:pk>', FuncionarioEdit.as_view(), name='update_funcionario'),
    path('deletar/<int:pk>', FuncionarioDelete.as_view(), name='delete_funcionario'),
    path('novo/', FuncionarioNovo.as_view(), name='create_funcionario'),
    path('relatorio_funcionarios/', relatorio_funcionarios, name='relatorio_funcionarios'),
    path('relatorio_funcionarios_html/', Pdf.as_view(), name='relatorio_funcionarios_html'),
]