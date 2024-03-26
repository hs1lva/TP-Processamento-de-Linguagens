
# Parte 1 - Gerar automato gráficamente usando a biblioteca graphviz

import json
from graphviz import Digraph

automato : dict = {}

with open("automato.json", "r", encoding="utf-8") as f:
    automato = json.load(f)

# Gerar o diagrama de grafos do automato
dot = Digraph(comment='Automato')

# 'none' para um node invisível
dot.node('start', shape='none', label='') 
# criar transcição incial
dot.edge('start', automato["q0"], label='')

# Criar os estados
for state in automato["delta"].keys():

    # caso o estado seja final
    if state in automato["F"]:
        dot.node(state, state, shape="doublecircle")

    else:
        dot.node(state, state, shape="circle")

# Criar as transições
for estado_inicial, transitions in automato["delta"].items():
    for simbolo, estado_final in transitions.items():
        dot.edge(estado_inicial, estado_final, label = simbolo)

# Visualização
dot.render('automaton_graph', view=True, format='png')


# Parte 2 - Gerar o código de funcionamento do automato
def reconhecedor(entrada : str, estado_inicial : str, transicoes : dict, estados_finais : list) -> bool:

    entrada : str = entrada.replace("ε", "")

    estado_atual : str = estado_inicial
    
    for char in entrada:
        # caso haja uma transição
        if char in transicoes[estado_atual]:
            estado_atual = transicoes[estado_atual][char]

        # caso haja uma transição com a palavra vazia
        elif "ε" in transicoes[estado_atual]:
            estado_atual_aux = transicoes[estado_atual]["ε"]
            if char in transicoes[estado_atual_aux]:
                estado_atual = transicoes[estado_atual_aux][char]
        else:
            # se não houver transição definida para este caracter de entrada, a palavra não é aceite
            return False
    return estado_atual in estados_finais

palavra : str = "aεεεεεcddddddddd"
estado_inicial : str = automato["q0"]
estados_finais : list = automato["F"]
transicoes : dict = automato["delta"]

reconhece : bool = reconhecedor(palavra, estado_inicial, transicoes, estados_finais)

if reconhece:
    print(f"A palavra '{palavra}' é aceite pelo automato.")
else:
    print(f"A palavra '{palavra}' não é aceite pelo automato.")
