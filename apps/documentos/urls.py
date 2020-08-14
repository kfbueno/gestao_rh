from django.urls import path
from .views import DocumentoCreate

    #FuncionariosList, FuncionarioEdit, FuncionarioDelete, FuncionarioNovo

urlpatterns = [
    path('novo/<int:funcionario_id>/', DocumentoCreate.as_view(), name='create_documento'),
#    path('deletar/<int:pk>', FuncionarioDelete.as_view(), name='delete_funcionario')


]