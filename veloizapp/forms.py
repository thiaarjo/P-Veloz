from django import forms
from .models import Tarefa, Comentario, Projeto

class adicionarTarefa(forms.ModelForm):
    projeto_texto = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Digite o nome do projeto'
        }),
        label="Projeto"
    )

    class Meta:
        model = Tarefa
        fields = ['descricao', 'categoria']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da tarefa'}),
            'categoria': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.responsavel = self.user  # CORREÇÃO AQUI
        
        projeto_nome = self.cleaned_data.get('projeto_texto')
        if projeto_nome:
            projeto, created = Projeto.objects.get_or_create(
                nome=projeto_nome,
                usuario=self.user,
                defaults={'tipo': 'outro', 'descricao': ''}
            )
            instance.projeto = projeto
        
        if commit:
            instance.save()
        return instance

class editarTarefa(forms.ModelForm):
    projeto_texto = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Projeto"
    )

    class Meta:
        model = Tarefa
        fields = ['descricao', 'categoria', 'status']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.projeto:
            self.fields['projeto_texto'].initial = self.instance.projeto.nome

    def save(self, commit=True):
        instance = super().save(commit=False)
        projeto_nome = self.cleaned_data.get('projeto_texto')
        
        if projeto_nome:
            projeto, created = Projeto.objects.get_or_create(
                nome=projeto_nome,
                usuario=instance.responsavel,
                defaults={'tipo': 'outro', 'descricao': ''}
            )
            instance.projeto = projeto
        else:
            instance.projeto = None
        
        if commit:
            instance.save()
        return instance

class comentarioTarefa(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['text_comment']
        labels = {
            'text_comment': 'Comentário'
        }
        widgets = {
            'text_comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Digite seu comentário...'})
        }

class adicionarProjeto(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'tipo', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do projeto'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descrição do projeto'})
        }

class editarProjeto(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'tipo', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }