import json
import argparse
import graphviz

def carregar_automato(ficheiro_definicao : str) -> dict:
    # Carrega o automato a partir do ficheiro JSON
    with open(ficheiro_definicao, 'r') as ficheiro:
        return json.load(ficheiro)

def gerar_grafo(automato : dict) -> graphviz.Digraph:
    grafo : graphviz.Digraph = graphviz.Digraph(format='png')

    # Adiciona os estados
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
            caminho.append(f"Não existe transição do estado {estado_atual} com o símbolo '{char}'.")
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

    args : argparse.Namespace = parser.parse_args()

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
            print("Situação de erro:", erro)

if __name__ == "__main__":
    main()


# Terminal ----> python3 1-AFD.py automato.json -graphviz (criar grafo png)
# Terminal ----> python3 1-AFD.py automato.json -rec 101 (reconhecer palavra)