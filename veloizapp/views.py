from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # ADICIONE ESTA LINHA
from django.contrib.auth.models import User
from .models import Tarefa, Comentario, Projeto
from .forms import adicionarTarefa, editarTarefa, comentarioTarefa, adicionarProjeto, editarProjeto

def login_view(request):
    if 'logout' in request.GET:
        logout(request)
        return redirect('login_page')
    
    if request.user.is_authenticated:
        return redirect('tarefas_pendentes')
    
    error = None
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('tarefas_pendentes')
            else:
                error = 'Usuário ou senha inválidos'
        
        elif 'cadastro' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST.get('email', '')
            
            if User.objects.filter(username=username).exists():
                error = 'Usuário já existe'
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                login(request, user)
                return redirect('tarefas_pendentes')
    
    return render(request, 'veloizapp/login_page.html', {'error': error})

# ADICIONE @login_required EM TODAS AS VIEWS ABAIXO:

@login_required
def projetos(request):
    projetos = Projeto.objects.filter(usuario=request.user)
    if request.method == 'POST':
        form = adicionarProjeto(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.usuario = request.user
            projeto.save()
            return redirect('projetos')
    else:
        form = adicionarProjeto()
    return render(request, 'veloizapp/projetos.html', {'projetos': projetos, 'form': form})

@login_required
def editar_projeto(request, projeto_id):
    projeto_obj = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    if request.method == 'POST':
        form = editarProjeto(request.POST, instance=projeto_obj)
        if form.is_valid():
            form.save()
            return redirect('projetos')
    else:
        form = editarProjeto(instance=projeto_obj)
    return render(request, 'veloizapp/editar_projeto.html', {'form': form, 'projeto': projeto_obj})

@login_required
def excluir_projeto(request, projeto_id):
    projeto_obj = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    projeto_obj.delete()
    return redirect('projetos')

@login_required
def detalhes_projeto(request, projeto_id):
    projeto_obj = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    tarefas_projeto = Tarefa.objects.filter(projeto=projeto_obj, responsavel=request.user)
    return render(request, 'veloizapp/detalhes_projeto.html', {
        'projeto': projeto_obj,
        'tarefas_projeto': tarefas_projeto
    })

@login_required  # ADICIONEI AQUI
def tarefas_pendentes(request):
    tarefas_pendentes = Tarefa.objects.filter(status='pendente', responsavel=request.user)

    if request.method == 'POST':
        if 'descricao' in request.POST:
            form = adicionarTarefa(request.POST, user=request.user)
            if form.is_valid():
                nova_tarefa = form.save()
                return redirect('tarefas_pendentes')

        elif 'text_comment' in request.POST and 'tarefa_id' in request.POST:
            tarefa_id = request.POST['tarefa_id']
            tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, responsavel=request.user)
            form = comentarioTarefa(request.POST)
            if form.is_valid():
                novo_comentario = form.save(commit=False)
                novo_comentario.tarefa = tarefa_obj
                novo_comentario.save()
                return redirect('tarefas_pendentes')
    else:
        form = adicionarTarefa(user=request.user)

    comentario_form = comentarioTarefa()

    return render(request, 'veloizapp/tarefas_pendentes.html', {
        'tarefas_pendentes': tarefas_pendentes,
        'form': form,
        'comentario_form': comentario_form
    })

@login_required
def iniciar_tarefa(request, tarefa_id):
    tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, responsavel=request.user)
    tarefa_obj.status = 'em andamento'
    tarefa_obj.save()
    return redirect('tarefas_pendentes')

@login_required
def concluir_tarefa(request, tarefa_id):
    tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, responsavel=request.user)
    tarefa_obj.status = 'concluida'
    tarefa_obj.save()
    return redirect('tarefas_pendentes')

@login_required
def excluir_tarefa(request, tarefa_id):
    tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, responsavel=request.user)
    tarefa_obj.delete()
    return redirect('tarefas_pendentes')

@login_required
def adiar_tarefa(request, tarefa_id):
    tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, responsavel=request.user)
    tarefa_obj.status = 'adiado'
    tarefa_obj.save()
    return redirect('tarefas_pendentes')

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, responsavel=request.user)
    if request.method == 'POST':
        form = editarTarefa(request.POST, instance=tarefa_obj)
        if form.is_valid():
            form.save()
            return redirect('tarefas_pendentes')
    else:
        form = editarTarefa(instance=tarefa_obj)
    return render(request, 'veloizapp/editar_tarefa.html', {'form': form, 'tarefa': tarefa_obj})

@login_required
def tarefas_concluidas(request):
    tarefas_concluidas = Tarefa.objects.filter(status='concluida', responsavel=request.user)
    return render(request, 'veloizapp/tarefas_concluidas.html', {'tarefas_concluidas': tarefas_concluidas})

@login_required
def tarefas_adiadas(request):
    tarefas_adiadas = Tarefa.objects.filter(status='adiado', responsavel=request.user)
    return render(request, 'veloizapp/tarefas_adiadas.html', {'tarefas_adiadas': tarefas_adiadas})

@login_required
def tarefas_andamento(request):
    tarefas_andamento = Tarefa.objects.filter(status='em andamento', responsavel=request.user)
    return render(request, 'veloizapp/tarefas_andamento.html', {'tarefas_andamento': tarefas_andamento})

@login_required
def mover_para_pendentes(request, tarefa_id):
    tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, responsavel=request.user)
    tarefa_obj.status = 'pendente'
    tarefa_obj.save()
    return redirect('tarefas_adiadas')

@login_required
def editar_comentario(request, comentario_id):
    comentario_obj = get_object_or_404(Comentario, id=comentario_id)
    if comentario_obj.tarefa.responsavel != request.user:
        return redirect('tarefas_pendentes')
    
    if request.method == 'POST':
        form = comentarioTarefa(request.POST, instance=comentario_obj)
        if form.is_valid():
            form.save()
            return redirect('tarefas_pendentes')
    else:
        form = comentarioTarefa(instance=comentario_obj)
    return render(request, 'veloizapp/editar_comentario.html', {'form': form, 'comentario': comentario_obj})

@login_required
def excluir_comentario(request, comentario_id):
    comentario_obj = get_object_or_404(Comentario, id=comentario_id)
    if comentario_obj.tarefa.responsavel == request.user:
        comentario_obj.delete()
    return redirect('tarefas_pendentes')