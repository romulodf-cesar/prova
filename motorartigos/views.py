from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from motorartigos.models import Responsavel,Comercio,EixoTecnologia
from django.db.models import Q # Importante para buscas complexas


def index(request):
    comercios_base = Comercio.objects.filter(publicada=True)
    
    # CORREÇÃO AQUI: Busca diretamente da tabela de eixos. 
    # Assim, virão apenas os 3 eixos cadastrados, sem duplicar!
    eixos = EixoTecnologia.objects.all()

    termo_busca = request.GET.get('busca')
    eixo_id = request.GET.get('eixo')

    comercios_todos = comercios_base

    # Se clicou em um eixo específico, filtra por ele
    if eixo_id:
        comercios_todos = comercios_todos.filter(id_fk_eixo__id=eixo_id)

    # Se digitou algo na barra de pesquisa
    if termo_busca:
        comercios_todos = comercios_todos.filter(
            Q(titulo__icontains=termo_busca) | 
            Q(texto__icontains=termo_busca) |
            Q(id_fk_responsavel__nome__icontains=termo_busca) |
            Q(id_fk_eixo__nome__icontains=termo_busca)
        )
    
    comercios_recentes = comercios_base.order_by('-data_publicacao')[:4]

    contexto = {
        'artigos': comercios_todos,
        'artigos_recentes': comercios_recentes,
        'eixos': eixos,                           
        'eixo_selecionado': eixo_id,               
        'termo_busca': termo_busca                 
    }
    return render(request, 'motorartigos/index.html', contexto)

def artigo(request):
    return render(request,'motorartigos/artigo.html')

def detalhe_comercio(request, id):
    comercio = get_object_or_404(
        Comercio.objects.select_related('id_fk_eixo', 'id_fk_responsavel'),
        id=id,
        publicada=True
    )
    return render(request, 'motorartigos/banca.html', {'artigo': comercio})
def mostrar_dashboard(request):
    return render(request, 'motorartigos/dashboard.html')

def criar_grafico_pizza():
    pass
    