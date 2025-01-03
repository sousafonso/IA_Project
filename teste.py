import os
import random
from modelos.localidade import Localidade
from modelos.rota import Rota
from modelos.grafo import Grafo
from modelos.transporte import Transporte
from algoritmos.bfs import bfs
from algoritmos.dfs import dfs
from algoritmos.a_star import a_star
from algoritmos.greedy import greedy_search
from algoritmos.custo_uniforme import uniform_cost_search
from utils.heuristica import heuristic
from utils.visualizacao import visualize_graph_with_image


grafo_complexo = Grafo()


localidades = [
    {"nome": "A", "populacao": 5000, "urgencia": 1, "acessibilidade": "asfalto", "mantimentos": 1200},
    {"nome": "B", "populacao": 4000, "urgencia": 3, "acessibilidade": "terra", "mantimentos": 15},
    {"nome": "C", "populacao": 3000, "urgencia": 8, "acessibilidade": "terra", "mantimentos": 25},
    {"nome": "D", "populacao": 2000, "urgencia": 10, "acessibilidade": "asfalto", "mantimentos": 30},
    {"nome": "E", "populacao": 6000, "urgencia": 2, "acessibilidade": "terra", "mantimentos": 10},
    {"nome": "F", "populacao": 3500, "urgencia": 5, "acessibilidade": "asfalto", "reabastecimento": True},
    {"nome": "G", "populacao": 4500, "urgencia": 7, "acessibilidade": "asfalto", "mantimentos": 40},
    {"nome": "H", "populacao": 2500, "urgencia": 9, "acessibilidade": "terra", "mantimentos": 20},
]

for loc in localidades:
    localidade = Localidade(
        nome=loc["nome"],
        populacao=loc["populacao"],
        urgencia=loc["urgencia"],
        acessibilidade=loc["acessibilidade"],
        reabastecimento=loc.get("reabastecimento", False),
    )
    localidade.add_mantimento(loc.get("mantimentos", 0))
    grafo_complexo.add_node(localidade)


rotas = [
    ("A", "B", 10, "asfalto"),      
    ("A", "C", 15, "terra"),
    ("B", "D", 20, "terra"),
    ("C", "E", 25, "terra"),
    ("D", "F", 30, "asfalto"),
    ("E", "G", 35, "asfalto"),
    ("F", "H", 40, "terra"),
    ("G", "H", 45, "terra"),
    ("C", "H", 50, "terra"),
    ("B", "E", 12, "terra"),
]

for origem, destino, distancia, pavimento in rotas:
    grafo_complexo.add_edge(origem, destino, distancia=distancia, pavimento=pavimento)


transporte_complexo = Transporte(tipo="camião", capacidade=1000, velocidade=80, autonomia=500)


resultado_dfs = uniform_cost_search(grafo_complexo, start="A",transport=transporte_complexo, )


print(resultado_dfs)
