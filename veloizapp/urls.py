from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_page'),
    path('projetos/', views.projetos, name='projetos'),
    path('projetos/<int:projeto_id>/editar/', views.editar_projeto, name='editar_projeto'),
    path('projetos/<int:projeto_id>/excluir/', views.excluir_projeto, name='excluir_projeto'),
    path('projetos/<int:projeto_id>/detalhes/', views.detalhes_projeto, name='detalhes_projeto'),
    path('tarefas/', views.tarefas_pendentes, name='tarefas_pendentes'),
    path('tarefas/concluidas/', views.tarefas_concluidas, name='tarefas_concluidas'),
    path('tarefas/adiadas/', views.tarefas_adiadas, name='tarefas_adiadas'),
    path('tarefas/andamento/', views.tarefas_andamento, name='tarefas_andamento'),
    path('tarefas/<int:tarefa_id>/iniciar/', views.iniciar_tarefa, name='iniciar_tarefa'),
    path('tarefas/<int:tarefa_id>/concluir/', views.concluir_tarefa, name='concluir_tarefa'),
    path('tarefas/<int:tarefa_id>/excluir/', views.excluir_tarefa, name='excluir_tarefa'),
    path('tarefas/<int:tarefa_id>/adiar/', views.adiar_tarefa, name='adiar_tarefa'),
    path('tarefas/<int:tarefa_id>/editar/', views.editar_tarefa, name='editar_tarefa'),
    path('comentario/<int:comentario_id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('comentario/<int:comentario_id>/excluir/', views.excluir_comentario, name='excluir_comentario'),
    path('tarefas/<int:tarefa_id>/mover-para-pendentes/', views.mover_para_pendentes, name='mover_para_pendentes'),
]