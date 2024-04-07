import json
import argparse
import graphviz

global contador
contador = 0

def change(set):
	return str(sorted(set)).replace('[', '{').replace(']', '}').replace('\'', '')



"""
	Convert the E-NFA to DFA from the transition table recursively
"""
def convert(automato, transacoes, alfabeto, estadoAtual, visited=None, result=None):
    global contador
    if result is None:
        result = {
            "Q": set(),  # Conjunto de estados
            "V": alfabeto,  # Alfabeto
            "q0": automato['q0'],  # Estado inicial
            "F": set(),  # Conjunto de estados finais
            "delta": {}  # Função de transição
        }

    keyNovoEstado = fechoE()




def carregar_automato(ficheiro_definicao : str) -> dict:
    # Carrega o automato a partir do ficheiro JSON
    with open(ficheiro_definicao, 'r') as ficheiro:
        return json.load(ficheiro)

def gerar_grafo(automato: dict) -> graphviz.Digraph:

    # Cria o grafo
    grafo: graphviz.Digraph = graphviz.Digraph(format='png')
    # Adiciona os estados ao grafo
    for estado in automato['Q']:
        if estado in automato['F']:
            grafo.node(estado, shape='doublecircle')
        else:
            grafo.node(estado, shape='circle')

    # Adiciona as transições ao grafo
    for estado, trans in automato['delta'].items():
        for simbolo, prox_estado in trans.items():
            grafo.edge(estado, prox_estado, label=simbolo)

    return grafo

def gravar_automato(automato: dict, ficheiro_automato: str) -> None:
    with open(ficheiro_automato, 'w') as ficheiro:
        json.dump(automato, ficheiro, indent=4)


def main():
    parser : argparse.ArgumentParser = argparse.ArgumentParser(description="Implementação de AFD")
    parser.add_argument('ficheiro_json', metavar='ficheiro_json', type=str,
                        help='O caminho para o ficheiro JSON contendo a definição do AFD')
    parser.add_argument('-graphviz', action='store_true',
                        help='Gerar a representação gráfica do grafo')
    parser.add_argument('-output', metavar='palavra', type=str,
                        help='Output JSON do AFD')

    args : argparse.Namespace = parser.parse_args()

    automato : dict = carregar_automato(args.ficheiro_json)
    #automato = validaAutomato(automato)

    if args.graphviz:
        grafo : graphviz.Digraph = gerar_grafo(automato)
        #verificar se é necessario gerar um ficheiro txt com estes dados
        print(grafo.source)  # Imprime a representação do grafo em formato DOT
        grafo.render('automatoAFD', view=True)  # Guarda e mostra o grafo em formato PNG

    if args.output:
        afd : dict = convert(automato, automato['delta'], automato['V'], [automato['q0']])
        print(afd)
        gravar_automato(afd, args.output)

if __name__ == "__main__":
    main()
