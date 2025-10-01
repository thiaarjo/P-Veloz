from django.db import models
from django.contrib.auth.models import User

class Projeto(models.Model):
    TIPOS_PROJETO = [
        ('pessoal', 'Pessoal'),
        ('trabalho', 'Trabalho'),
        ('estudos', 'Estudos'),
        ('saude', 'Saúde'),
        ('financas', 'Finanças'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_PROJETO, default='pessoal')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projetos")

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    TIPO_STATUS = [
        ('pendente', 'Pendente'),
        ('em andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('adiado', 'Adiado'),
    ]

    OPCOES_CATEGORIA = [
        ('urgente', 'Urgente'),
        ('importante', 'Importante'),
        ('precisa ser feito', 'Precisa ser feito'),
        ('pode ser adiado', 'Pode ser adiado'),
    ]

    descricao = models.CharField(max_length=150)
    data_criacao = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=50, choices=OPCOES_CATEGORIA, default='importante')
    status = models.CharField(max_length=20, choices=TIPO_STATUS, default='pendente')
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tarefas")
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="tarefas", null=True)

    def __str__(self):
        return f"{self.descricao} ({self.status})"

class Comentario(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='comentarios')
    text_comment = models.TextField(max_length=1500)
    data_comentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_comentario']

    def __str__(self):
        return f"Comentário em {self.tarefa.descricao} - {self.data_comentario.strftime('%Y-%m-%d %H:%M')}"