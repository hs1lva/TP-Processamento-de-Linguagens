# AFD - Autómato Finito Determinístico

import json
import argparse
import graphviz
from graphviz import Digraph
import os

def carregar_automato(ficheiro_definicao : str) -> dict:
    # Verifica se o ficheiro existe
    diretorio_atual = os.getcwd()
    caminho_completo = os.path.join(diretorio_atual, ficheiro_definicao)
    
    if not os.path.isfile(caminho_completo):
        print(f"O ficheiro '{ficheiro_definicao}' não existe.")
        exit()

    # Carrega o automato a partir do ficheiro JSON
    try:
        with open(ficheiro_definicao, 'r') as ficheiro:
            return json.load(ficheiro)
    except Exception as e:
        print(f"Erro ao carregar o automato.{e}")
    

def gerar_grafo(automato : dict) -> graphviz.Digraph:
    # Verifica condições essenciais
    if automato['q0'] == '':
        print("O automato não tem estado inicial.")
        exit()
    if automato['F'] == '':
        print("O automato não tem estado final.")
        exit()
    if automato['delta'] == '':
        print("O automato não tem transições.")
        exit()
    
    # Cria o grafo
    grafo : graphviz.Digraph = graphviz.Digraph(format='png')


    # Cria estados, caso não existam
    if automato['Q'] == '':
        grafo.node('start', shape='none', label='')
        grafo.edge('start', automato['q0'], shape='none', label='')

        for estado in automato['delta']:
            if estado in automato['F']:
                grafo.node(estado, shape='doublecircle')
            else:
                grafo.node(estado)
    else:
        # Adiciona os estados se já existirem
        for estado in automato['Q']:
            if estado in automato['F']:
                grafo.node(estado, shape='doublecircle')
            else:
                grafo.node(estado)

    # Adiciona as transições
    for estado, trans in automato['delta'].items():
        for simbolo, prox_estado in trans.items():
            grafo.edge(estado, prox_estado, label=simbolo)

    return grafo

def reconhecer_palavra(automato : dict, palavra : str) -> tuple[bool, list, str | None]:
    estado_atual : str = automato['q0']
    caminho : list = [estado_atual]

    for char in palavra:
        try:
            prox_estado : str = automato['delta'][estado_atual][char]
            caminho.append(prox_estado)
            estado_atual = prox_estado
        except KeyError:
            return False, caminho, f"Não há transição do estado {estado_atual} com o símbolo '{char}'."

    if estado_atual in automato['F']:
        return True, caminho, None
    else:
        return False, caminho, f"O estado {estado_atual} não é um estado final."

def main():
    parser = argparse.ArgumentParser(description="Implementação de AFD")
    parser.add_argument('ficheiro_json', metavar='ficheiro_json', type=str,
                        help='O caminho para o ficheiro JSON contendo a definição do AFD')
    parser.add_argument('-graphviz', action='store_true',
                        help='Gerar a representação gráfica do grafo')
    parser.add_argument('-rec', metavar='palavra', type=str,
                        help='Reconhecer uma palavra')
    
    args = parser.parse_args()

    automato : dict = carregar_automato(args.ficheiro_json)

    if args.graphviz:
        grafo : graphviz.Digraph = gerar_grafo(automato)
        print(grafo.source)  # Imprime a representação do grafo em formato DOT
        grafo.render('automatoAFD', view=True)  # Guarda e mostra o grafo em formato PNG

    if args.rec:
        reconhecido : bool
        caminho : list
        erro : str | None
        reconhecido, caminho, erro = reconhecer_palavra(automato, args.rec)
        if reconhecido:
            print(f"A palavra '{args.rec}' é reconhecida.")
            print("Caminho percorrido:", ' -> '.join(caminho))
        else:
            print(f"A palavra '{args.rec}' não é reconhecida.")
            print("Caminho percorrido:", ' -> '.join(caminho))
            print("Situação de erro:", erro)

if __name__ == "__main__":
    main()


# Terminal ----> python3 1-AFD.py automato.json -graphviz (criar grafo png)
# Terminal ----> python3 1-AFD.py automato.json -rec 101 (reconhecer palavra)